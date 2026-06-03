from sqlalchemy import Column, String, Text, Integer, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.base_model import BaseModel
from app.models.enums import VisibilityEnum


class Book(BaseModel):
    __tablename__ = "books"
    slug = Column(String(255), unique=True, nullable=False)
    title_bn = Column(String(500), nullable=False)
    title_en = Column(String(500), nullable=True)
    title_ar = Column(String(500), nullable=True)
    description_bn = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    cover_url = Column(String(1000), nullable=True)
    isbn = Column(String(100), nullable=True)
    pages = Column(Integer, nullable=True)
    published_year = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(10), default="BDT")
    language = Column(String(50), nullable=True)
    visibility = Column(
        Enum(VisibilityEnum), default=VisibilityEnum.PUBLIC, nullable=False
    )
    publisher_id = Column(
        UUID(as_uuid=True), ForeignKey("publishers.id"), nullable=True
    )
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    book_metadata = Column(JSONB, nullable=True)
    user_books = relationship("UserBook", back_populates="book")
    publisher = relationship("Publisher", back_populates="books")
    book_authors = relationship("BookAuthor", back_populates="book")
    owner = relationship("User", back_populates="owned_books")
    book_tags = relationship("BookTag", back_populates="book")
    book_shelves = relationship("BookShelf", back_populates="book")
    wishlists = relationship("Wishlist", back_populates="book")
    lending_records = relationship("LendingRecord", back_populates="book")
