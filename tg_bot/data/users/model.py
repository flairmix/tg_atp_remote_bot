from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date, Time, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, relationship
from datetime import date
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass

@dataclass
class User(Base):
    __tablename__ = "user_account"
    shortname: Mapped[str] = mapped_column(String, unique=True) 
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    group: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, nullable=False)
    GRL: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    chat_id: Mapped[Optional[int]] = mapped_column(String, nullable=False)
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid4, primary_key=True)
    user_status: Mapped[List["Status"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", default_factory=list
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.shortname!r}, fullname={self.fullname!r})"


@dataclass
class Status(Base):
    __tablename__ = "work_status"

    work_status: Mapped[str]= mapped_column(String, nullable=False)
    date_message: Mapped[date] = mapped_column(DateTime)
    message: Mapped[str]= mapped_column(String, nullable=False)
    date_for_request: Mapped[date] = mapped_column(Date)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="user_status")
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid4, primary_key=True)
    
    def __post_init__(self):
        if self.user is None:
            raise ValueError("A Status must be associated with a User instance.")

    def __repr__(self) -> str:
        return f"user(id={self.user!r}, work_status={self.work_status!r})"
