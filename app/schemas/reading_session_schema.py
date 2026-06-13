from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ReadingSessionCreate(BaseModel):
    book_id: UUID

    pages_read: int

    started_at: datetime
    ended_at: datetime | None = None


class ReadingSessionResponse(BaseModel):
    id: UUID

    user_id: UUID
    book_id: UUID

    pages_read: int

    started_at: datetime
    ended_at: datetime | None

    class Config:
        from_attributes = True
