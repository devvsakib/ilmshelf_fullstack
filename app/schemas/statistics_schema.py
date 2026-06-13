from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    total_books: int
    completed_books: int

    reading_books: int

    completion_rate: float
