from boto3 import client
from botocore.exceptions import ClientError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import crud, schemas


def create_user_handler(db: Session, user: schemas.UserCreate):
    exist = crud.get_user_by_email(db=db, email=user.email)
    if exist:
        raise UserWarning("User already exists")

    return crud.create_user(db=db, user=user)


def generate_upload_signed_url(image_name: str):
    s3 = client("s3", region_name="ap-south-1")
    try:
        return s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": "carthage-user-assets", "Key": f"users/{image_name}.jpg"},
            ExpiresIn=3600,
            HttpMethod='PUT',
        )

    except ClientError as e:
        print(f"Couldn't generate presigned URL: {e}")
        return None


def get_user_avatar_url(image_name: str) -> str | None:
    # get profile image from s3
    s3 = client("s3", region_name="ap-south-1")

    try:
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": "carthage-user-assets", "Key": f"users/{image_name}.jpg"},
            ExpiresIn=3600,
            HttpMethod="GET"
        )

    except ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))
