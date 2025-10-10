import json

from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session

from controller import users
from repository import crud, schemas
from repository.db import get_db

route = APIRouter()


@route.get("", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@route.post("", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = users.create_user_handler(db, user)
    except UserWarning as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"error {str(e)}"
        )
    return user


@route.get("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.avatar_url = users.get_user_avatar_url(str(user_id))

    return user


@route.put("/{user_id}", response_model=schemas.User, status_code=201)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    update = crud.update_user(db=db, user_id=user_id, user=user)

    if update is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(
        content='{"message": "User updated successfully"}',
        status_code=status.HTTP_201_CREATED,
    )


@route.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_user(db=db, user_id=user_id)

    if delete is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(
        content='{"message": "User deleted successfully"}',
        status_code=status.HTTP_204_NO_CONTENT,
    )


@route.post("/{user_id}/upload", status_code=status.HTTP_201_CREATED)
def get_upload_presigned_url(user_id: int):
    url_response = users.generate_upload_signed_url(str(user_id))

    print("=-=" * 10)
    print(url_response)
    print("=-=" * 10)

    return Response(content=json.dumps(url_response))
