from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class LendingRecordCreate(BaseModel):
    book_id: UUID

    borrower_name: str
    borrower_phone: str | None = None

    due_date: datetime | None = None


class LendingRecordResponse(BaseModel):
    id: UUID

    book_id: UUID
    user_id: UUID

    borrower_name: str
    borrower_phone: str | None

    due_date: datetime | None

    returned_at: datetime | None

    created_at: datetime

    class Config:
        from_attributes = True
