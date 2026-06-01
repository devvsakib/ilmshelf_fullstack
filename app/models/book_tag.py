from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class BookTag(BaseModel):
    __tablename__ = "book_tags"
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)
    book = relationship("Book", back_populates="book_tags")
    tag = relationship("Tag", back_populates="book_tags")
