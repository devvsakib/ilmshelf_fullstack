from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    total_books: int
    completed_books: int
    reading_books: int
    completion_rate: float


class MonthlyStatisticsResponse(BaseModel):
    month: str

    sessions: int
    pages_read: int

    reading_hours: float


class YearlyStatisticsResponse(BaseModel):
    year: int

    sessions: int
    pages_read: int

    reading_hours: float
