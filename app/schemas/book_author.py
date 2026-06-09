from uuid import UUID

from pydantic import BaseModel
from app.models.enums import AuthorRoleEnum


class BookAuthorCreate(BaseModel):
    author_id: UUID
    role: AuthorRoleEnum
