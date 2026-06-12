from uuid import UUID
from pydantic import BaseModel


class PersonInfo(BaseModel):
    id: UUID
    name_bn: str
    name_en: str | None = None
    name_ar: str | None = None


class PublisherInfo(BaseModel):
    id: UUID
    name: str


class TagInfo(BaseModel):
    id: UUID
    name: str
    slug: str


class BookDetailsResponse(BaseModel):
    id: UUID

    title_bn: str | None = None
    title_en: str | None = None
    title_ar: str | None = None

    cover_url: str | None = None

    authors: list[PersonInfo]
    translators: list[PersonInfo]
    editors: list[PersonInfo]

    publisher: PublisherInfo | None

    tags: list[TagInfo]

    wishlist_count: int
    reader_count: int
