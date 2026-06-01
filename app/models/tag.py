from sqlalchemy import Column, String
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship


class Tag(BaseModel):
    __tablename__ = "tags"

    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)

    book_tags = relationship("BookTag", back_populates="tag")
