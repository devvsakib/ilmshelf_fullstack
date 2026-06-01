from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from app.models.enums import ShelfTypeEnum


class Shelf(BaseModel):
    __tablename__ = "shelves"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    type = Column(Enum(ShelfTypeEnum), nullable=False)
    is_public = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    creator = relationship("User", back_populates="shelves")
    book_shelves = relationship("BookShelf", back_populates="shelf")
