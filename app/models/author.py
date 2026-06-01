from sqlalchemy import Column, String, Text
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship

class Author(BaseModel):
    __tablename__ = "authors"

    name_bn = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_ar = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    book_authors = relationship("BookAuthor", back_populates="author")
