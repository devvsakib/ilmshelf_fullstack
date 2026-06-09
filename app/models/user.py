from sqlalchemy import Column, String, Boolean, Enum
from app.models.base_model import BaseModel
from app.models.enums import RoleEnum
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)
    user_books = relationship("UserBook", back_populates="user")
    shelves = relationship("Shelf", back_populates="creator")
    wishlists = relationship("Wishlist", back_populates="user")
    reading_goals = relationship("ReadingGoal", back_populates="user")
    lending_records = relationship("LendingRecord", back_populates="user")
    owned_books = relationship("Book", back_populates="owner")
