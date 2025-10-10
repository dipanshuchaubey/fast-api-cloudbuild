from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from repository.db import get_db
from sqlalchemy.orm import Session
from repository import models, schemas
import json

route = APIRouter()


class LoginBody(BaseModel):
    username: str
    password: str


@route.post("/login")
def login(creds: LoginBody, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == creds.username).first()
    if user is None:
        return Response(
            status_code=401,
            content=json.dumps({"error": "Invalid username or password"}),
            headers={"content-type": "application/json"},
        )
    return {"login": user}


@route.post("/whoami")
def whoami():
    return {"whoami": {}}
