from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    total_users: int
    total_books: int

    total_authors: int
    total_publishers: int
    total_tags: int

    total_shelves: int

    total_notes: int
    total_highlights: int

    total_wishlists: int
    total_reading_goals: int
