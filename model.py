from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    shortname: Mapped[str] = mapped_column(String(5))
    fullname: Mapped[Optional[str]]
    email_address: Mapped[str]
    group: Mapped[Optional[str]]
    GRL: Mapped[Optional[str]]
    user_status: Mapped[List["Status"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"

    # addresses: Mapped[List["Address"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
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
    date_status: Mapped[date] = mapped_column(Date)
    message: Mapped[str] 
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="user_status")
    

    def __repr__(self) -> str:
        return f"user(id={self.user!r}, work_status={self.work_status!r})"
