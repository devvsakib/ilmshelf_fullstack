from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.enums import ShelfTypeEnum


class ShelfCreate(BaseModel):
    name: str
    type: ShelfTypeEnum
    is_public: bool = True


class ShelfResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    type: ShelfTypeEnum
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True
