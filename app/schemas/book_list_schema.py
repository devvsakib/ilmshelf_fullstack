from pydantic import BaseModel
from uuid import UUID


class BookListItem(BaseModel):
    id: UUID

    title_bn: str | None = None
    title_en: str | None = None
    title_ar: str | None = None

    cover_url: str | None = None
    slug: str


class BookListResponse(BaseModel):
    items: list[BookListItem]

    page: int
    limit: int

    total: int
    pages: int
