from sqlalchemy import Column, Integer, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from app.models.enums import ReadStatusEnum


class UserBook(BaseModel):
    __tablename__ = "user_books"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    shelf_id = Column(UUID(as_uuid=True), ForeignKey("shelves.id"), nullable=True)
    read_status = Column(
        Enum(ReadStatusEnum), default=ReadStatusEnum.NOT_STARTED, nullable=False
    )
    current_page = Column(Integer, default=0)
    rating = Column(Integer, nullable=True)
    is_private = Column(Boolean, default=False)
    purchase_date = Column(Date, nullable=True)
    reading_started_at = Column(DateTime, nullable=True)
    reading_completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_books")
    book = relationship("Book", back_populates="user_books")
    notes = relationship("Note", back_populates="user_book")
    highlights = relationship("Highlight", back_populates="user_book")
