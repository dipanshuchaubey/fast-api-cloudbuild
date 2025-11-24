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

# 1. Check for multiple heads
echo "Checking for multiple migration heads..."
HEADS=$(alembic heads 2>&1)
HEAD_COUNT=$(echo "$HEADS" | grep -E "^[a-f0-9]+ \(head\)" | wc -l)

echo "$HEADS"

if [ "$HEAD_COUNT" -gt 1 ]; then
    echo -e "${RED}❌ ERROR: Multiple migration heads detected!${NC}"
    echo ""
    echo "This means there's a migration conflict. To fix:"
    echo "Sync your branch with the main branch and recreate your migration:"
    echo "  1. Delete your migration file(s) in alembic/versions/"
    echo "  2. merge main into your branch"
    echo "  3. Recreate your migration: alembic revision --autogenerate -m 'your message'"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ Single migration head found${NC}"
fi

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
echo -e "${GREEN}✨ All migration checks passed!${NC}"
