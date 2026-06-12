from pydantic import BaseModel


class DashboardResponse(BaseModel):
    books_owned: int
    books_completed: int
    currently_reading: int

    wishlist_count: int

    notes_count: int
    highlights_count: int

    goal_target: int
    goal_completed: int
