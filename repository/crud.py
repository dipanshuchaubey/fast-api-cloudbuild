from sqlalchemy.orm import Session
from ulid import ULID

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password_hash = user.password + "notreallyhashed"
    user = models.User(
        email=user.email, tenant_id=user.tenant_id, hashed_password=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None

    existing_user.hashed_password = user.password + "notreallyhashed"
    db.commit()
    db.refresh(existing_user)

    return existing_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Item)
        .filter(models.Item.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    item = models.Item(**item.model_dump(), owner_id=user_id)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_requisitions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Requisition).offset(skip).limit(limit).all()


def get_requisitions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Requisition).filter(models.Requisition.created_by == user_id).offset(skip).limit(limit).all()


def create_requisition(db: Session, body: schemas.RequisitionCreate, user_id: int):
    requisition = models.Requisition(
        requisition_id=str(ULID()),
        tenant_id=123,
        requisition_title=body.requisition_title,
        status="CREATED",
        created_by=user_id,
    )

    db.add(requisition)
    db.commit()
    db.refresh(requisition)

    return requisition
