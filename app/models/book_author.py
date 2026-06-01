from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel
from app.models.enums import AuthorRoleEnum

from sqlalchemy.orm import relationship


class BookAuthor(BaseModel):
    __tablename__ = "book_authors"

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)

    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="book_authors")

    book = relationship("Book", back_populates="book_authors")
    role = Column(Enum(AuthorRoleEnum), nullable=False)
