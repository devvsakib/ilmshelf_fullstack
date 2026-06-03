from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# user_book_id = current logged in user, mean MY
class NoteCreate(BaseModel):
    user_book_id: UUID
    page: int | None = None
    content: str


class NoteUpdate(BaseModel):
    page: int | None = None
    content: str
    is_public: bool | None = None


class NoteResponse(BaseModel):
    id: UUID

    user_book_id: UUID
    page: int | None = None
    content: str
    is_public: bool
    created_at: datetime

    class config:
        from_attributes = True
