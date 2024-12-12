from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date, Time, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, relationship
from datetime import date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    # id: Mapped[UUID] = mapped_column(primary_key=True)
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    shortname: Mapped[str] = mapped_column(String, unique=True)
    fullname: Mapped[str] 
    email: Mapped[str] 
    group: Mapped[str] 
    GRL: Mapped[Optional[str]] 
    city: Mapped[Optional[str]] 
    user_status: Mapped[List["Status"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", 
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.shortname!r}, fullname={self.fullname!r})"


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

class Status(Base):
    __tablename__ = "work_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_status: Mapped[str]
    date_message: Mapped[date] = mapped_column(DateTime)
    message: Mapped[str]
    date_for_request: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="user_status")
    

    def __repr__(self) -> str:
        return f"user(id={self.user!r}, work_status={self.work_status!r})"
