from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('ix_users_email_tenant_id', 'email', 'tenant_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Requisition(Base):
    __tablename__ = "requisitions"
    __table_args__ = (
        Index('ix_requisitions_tenant_id_status', 'tenant_id', 'status'),
    )

    requisition_id = Column(String, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    requisition_title = Column(String, nullable=False)
    status = Column(String, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    __table_args__ = (
        Index('ix_purchase_orders_po_id_tenant_id', 'po_id', 'tenant_id'),
    )

    po_id = Column(String, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    po_title = Column(String, nullable=False)
    status = Column(String, nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)