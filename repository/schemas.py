from datetime import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    tenant_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    avatar_url: str = None

    class Config:
        from_attributes = True


class RequisitionBase(BaseModel):
    requisition_title: str


class RequisitionCreate(RequisitionBase):
    pass


class Requisition(RequisitionBase):
    requisition_id: str
    tenant_id: int
    status: str

    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
