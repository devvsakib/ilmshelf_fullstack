from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class HighlightCreate(BaseModel):
    user_book_id: UUID

    page: int | None = None
    selected_text: str
    note: str | None = None


class HighlightUpdate(BaseModel):
    page: int | None = None
    selected_text: str
    note: str | None = None


class HighlightResponse(BaseModel):
    id: UUID
    user_book_id: UUID

    page: int | None = None
    selected_text: str
    note: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
