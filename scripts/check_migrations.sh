#!/bin/bash
# Script to check for Alembic migration conflicts

set -e

echo "🔍 Checking Alembic migrations for conflicts..."
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if alembic is installed
if ! command -v alembic &> /dev/null; then
    echo -e "${RED}❌ Alembic is not installed. Please install it first.${NC}"
    echo "   pip install alembic"
    exit 1
fi

EVENT_NAME="${1:-push}"
BASE_REF="${2:-main}"

# 1. Check for multiple heads
echo "Checking for multiple migration heads..."

if [ "$EVENT_NAME" = "pull_request" ]; then
  echo "Simulating merge with base branch to detect conflicts..."
  
  # Get current PR migrations
  echo "PR branch migrations:"
  ls -1 alembic/versions/*.py 2>/dev/null | grep -v __pycache__ || true
  echo ""
  
  # Fetch and get main branch migrations
  git fetch origin "$BASE_REF"
  echo "Fetching main branch migrations..."
  git checkout "origin/$BASE_REF" -- alembic/versions/
  
  echo "Main branch migrations:"
  ls -1 alembic/versions/*.py 2>/dev/null | grep -v __pycache__ || true
  echo ""
  
  # Now we have BOTH sets of migrations - check for multiple heads
  echo "Checking combined migrations (simulated merge)..."
  HEADS=$(alembic heads 2>&1)
  HEAD_COUNT=$(echo "$HEADS" | grep -E "^[a-f0-9]+ \(head\)" | wc -l)
  
  echo "Combined migration heads:"
  echo "$HEADS"
  echo ""
  echo "Number of heads: $HEAD_COUNT"
  
  if [ "$HEAD_COUNT" -gt 1 ]; then
    echo -e "${RED}❌ ERROR: Multiple migration heads detected after merge!${NC}"
    echo "This indicates a migration conflict between your PR and $BASE_REF."
    echo ""
    echo "To fix this:"
    echo "1. Pull the latest changes from $BASE_REF"
    echo "2. Merge/rebase with $BASE_REF"
    echo "3. Manually resolve migration conflicts"
    echo ""
    exit 1
  fi
  
  # Restore PR state
  git checkout HEAD -- alembic/versions/
else
  # For push to main, just check current state
  HEADS=$(alembic heads 2>&1)
  HEAD_COUNT=$(echo "$HEADS" | grep -E "^[a-f0-9]+ \(head\)" | wc -l)

  echo "Migration heads found:"
  echo "$HEADS"
  echo ""
  echo "Number of heads: $HEAD_COUNT"

  if [ "$HEAD_COUNT" -gt 1 ]; then
    echo -e "${RED}❌ ERROR: Multiple migration heads detected!${NC}"
    echo "This indicates a migration conflict."
    exit 1
  fi
fi

echo -e "${GREEN}✅ Single migration head found${NC}"
echo ""

# 2. Check for duplicate revision IDs
echo "Checking for duplicate revision IDs..."
DUPLICATES=$(grep -r "^revision.*=.*['\"]" alembic/versions/*.py 2>/dev/null | \
             sed "s/.*['\"]\\([a-f0-9]*\\)['\"].*/\\1/" | \
             sort | uniq -d)

if [ -n "$DUPLICATES" ]; then
    echo -e "${RED}❌ Duplicate revision IDs found:${NC}"
    echo "$DUPLICATES"
    exit 1
else
    echo -e "${GREEN}✅ No duplicate revision IDs${NC}"
fi

echo ""

# 3. Compare with base branch (PR only)
if [ "$EVENT_NAME" = "pull_request" ]; then
  echo "Checking migrations against base branch..."
  echo "Base branch: $BASE_REF"

  # Get the merge base
  git fetch origin "$BASE_REF"
  MERGE_BASE=$(git merge-base HEAD "origin/$BASE_REF")

  # Get new migration files in this PR
  NEW_MIGRATIONS=$(git diff --name-only "$MERGE_BASE" HEAD -- alembic/versions/ | grep "\.py$" | grep -v __pycache__ || true)

  if [ -n "$NEW_MIGRATIONS" ]; then
    echo "New migrations in this PR:"
    echo "$NEW_MIGRATIONS"
    echo ""
    
    # For each new migration, check its down_revision
    for migration in $NEW_MIGRATIONS; do
      echo "Checking $migration..."
      DOWN_REV=$(grep "down_revision.*=.*['\"]" "$migration" | sed "s/.*['\"]\\([a-f0-9]*\\)['\"].*/\\1/" | head -1)
      
      if [ "$DOWN_REV" != "None" ] && [ -n "$DOWN_REV" ]; then
        echo "  Down revision: $DOWN_REV"
        
        # Check if the parent revision exists in base branch
        git checkout "origin/$BASE_REF" -- alembic/versions/ 2>/dev/null || true
        
        PARENT_EXISTS=$(grep -l "revision.*=.*['\"]$DOWN_REV['\"]" alembic/versions/*.py 2>/dev/null || echo "")
        
        # Restore current branch migrations
        git checkout HEAD -- alembic/versions/
        
        if [ -z "$PARENT_EXISTS" ]; then
          echo -e "  ${YELLOW}⚠️  Warning: Parent revision $DOWN_REV not found in base branch${NC}"
          echo "  This might indicate you need to rebase on the latest changes"
        else
          echo -e "  ${GREEN}✅ Parent revision exists in base branch${NC}"
        fi
      fi
    done
  else
    echo "No new migrations found in this PR."
  fi
  echo ""
fi

echo -e "${GREEN}✨ All migration checks passed!${NC}"
