from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Publisher(BaseModel):
    __tablename__ = "publishers"

    name = Column(String(255), nullable=False)
    website = Column(String(500), nullable=True)
    books = relationship("Book", back_populates="publisher")
