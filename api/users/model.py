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
class Users(Base):
    __tablename__ = "users"
    # shortname: Mapped[str] = mapped_column(String, unique=True) 
    id: Mapped[str] = mapped_column(String, unique=True, primary_key=True) 
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    group: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, nullable=False)
    GRL: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    chat_id: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid4, primary_key=True)
    
    user_requests: Mapped[List["User_requests"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", default_factory=list
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.shortname!r}, fullname={self.fullname!r})"


@dataclass
class User_requests(Base):
    __tablename__ = "user_requests"

    work_status: Mapped[str]= mapped_column(String, nullable=False)
    date_message: Mapped[date] = mapped_column(DateTime)
    message: Mapped[str]= mapped_column(String, nullable=False)
    date_for_request: Mapped[date] = mapped_column(Date)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="user_requests")
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid4, primary_key=True)
    
    def __post_init__(self):
        if self.user is None:
            raise ValueError("A Status must be associated with a User instance.")

    def __repr__(self) -> str:
        return f"user(id={self.user!r}, work_status={self.work_status!r})"
