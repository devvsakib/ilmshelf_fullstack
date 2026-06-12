from uuid import UUID
from pydantic import BaseModel


class PublicProfileResponse(BaseModel):
    id: UUID

    username: str
    full_name: str

    books_count: int
    completed_books: int

    shelves_count: int
