from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.models.enums import AuthorRoleEnum


class BookAuthorCreate(BaseModel):
    author_id: UUID
    role: AuthorRoleEnum


class BookAuthorResponse(BaseModel):
    id: UUID

    author_id: UUID
    book_id: UUID

    role: AuthorRoleEnum

    created_at: datetime

    class Config:
        from_attributes = True
