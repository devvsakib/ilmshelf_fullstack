from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel
from app.models.enums import ReadStatusEnum


class UserBookCreate(BaseModel):
    book_id: UUID
    shelf_id: UUID | None = None


class UserBookUpdate(BaseModel):
    shelf_id: UUID | None = None
    read_status: ReadStatusEnum | None = None
    current_page: int | None = None
    rating: int | None = None
    is_private: bool | None = None
    purchase_date: date | None = None


class UserBookResponse(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    shelf_id: UUID | None
    read_status: ReadStatusEnum
    current_page: int
    rating: int | None
    is_private: bool
    purchase_date: date | None
    reading_started_at: datetime | None
    reading_completed_at: datetime | None
    created_at: datetime
    class Config:
        from_attributes = True
