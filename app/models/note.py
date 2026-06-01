from sqlalchemy import (
    Column,
    Text,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Note(BaseModel):
    __tablename__ = "notes"

    user_book_id = Column(
        UUID(as_uuid=True), ForeignKey("user_books.id"), nullable=False
    )
    user_book = relationship("UserBook", back_populates="notes")
    page = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    is_public = Column(Boolean, default=False)
