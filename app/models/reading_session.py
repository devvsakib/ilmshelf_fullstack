from sqlalchemy import Column, Integer, ForeignKey, DateTime

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class ReadingSession(BaseModel):
    __tablename__ = "reading_sessions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)

    pages_read = Column(Integer, nullable=False, default=0)

    started_at = Column(DateTime, nullable=False)

    ended_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="reading_sessions")

    book = relationship("Book")
