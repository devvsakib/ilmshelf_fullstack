from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BookTagCreate(BaseModel):
    tag_id: UUID


class BookTagResponse(BaseModel):
    id: UUID
    book_id: UUID
    tag_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
