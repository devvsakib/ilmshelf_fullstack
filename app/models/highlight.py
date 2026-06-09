from sqlalchemy import Column, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel


class Highlight(BaseModel):
    __tablename__ = "highlights"

    user_book_id = Column(
        UUID(as_uuid=True), ForeignKey("user_books.id"), nullable=False
    )
    user_book = relationship("UserBook", back_populates="highlights")
    page = Column(Integer, nullable=True)

    selected_text = Column(Text, nullable=False)
    is_public = Column(Boolean, default=False)
    note = Column(Text, nullable=True)
