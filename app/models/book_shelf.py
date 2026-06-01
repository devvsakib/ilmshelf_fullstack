from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class BookShelf(BaseModel):
    __tablename__ = "book_shelves"

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    shelf_id = Column(UUID(as_uuid=True), ForeignKey("shelves.id"), nullable=False)
    book = relationship("Book", back_populates="book_shelves")
    shelf = relationship("Shelf", back_populates="book_shelves")
