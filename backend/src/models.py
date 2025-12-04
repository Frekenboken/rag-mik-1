from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime, UTC

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

