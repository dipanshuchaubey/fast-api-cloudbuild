from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from repository import crud, schemas
from repository.db import get_db

route = APIRouter()


@route.get("", response_model=list[schemas.Requisition], status_code=status.HTTP_200_OK)
def get_requisitions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_requisitions(db, skip=skip, limit=limit)


@route.post("", response_model=schemas.Requisition, status_code=status.HTTP_201_CREATED)
def create_requisition(body: schemas.RequisitionCreate, db: Session = Depends(get_db)):
    return crud.create_requisition(db, body=body, user_id=1)


@route.put("/{requisition_id}")
def update_requisition(requisition_id: int):
    return {"requisition": {"id": requisition_id}}


@route.delete("/{requisition_id}")
def delete_requisition(requisition_id: int):
    return {"requisition": {"id": requisition_id}}
