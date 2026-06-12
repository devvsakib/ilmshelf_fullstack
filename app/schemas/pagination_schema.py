from pydantic import BaseModel


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
