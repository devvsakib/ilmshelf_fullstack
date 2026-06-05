from uuid import UUID
from pydantic import BaseModel


class ReadingGoalCreate(BaseModel):
    year: int
    target_books: int


class ReadingGoalUpdate(BaseModel):
    target_books: int | None = None
    completed_books: int


class ReadingGoalResponse(BaseModel):
    id: UUID
    year: int
    target_books: int
    completed_books: int

    class Config:
        from_attributes = True
