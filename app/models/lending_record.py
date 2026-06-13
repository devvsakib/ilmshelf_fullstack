from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class LendingRecord(BaseModel):
    __tablename__ = "lending_records"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String(255), nullable=False)
    borrower_phone = Column(String(50), nullable=True)
    due_date = Column(DateTime, nullable=True)
    borrower_phone = Column(String(50), nullable=True)
    user = relationship("User", back_populates="lending_records")
    book = relationship("Book", back_populates="lending_records")
