from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class ReadingGoal(BaseModel):
    __tablename__ = "reading_goals"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    year = Column(Integer, nullable=False)
    target_books = Column(Integer, nullable=False)
    completed_books = Column(Integer, default=0)

    user = relationship("User", back_populates="reading_goals")
