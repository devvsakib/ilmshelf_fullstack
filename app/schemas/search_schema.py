from uuid import UUID
from pydantic import BaseModel


class SearchBookResponse(BaseModel):
    id: UUID
    slug: str

    title_bn: str | None = None
    title_en: str | None = None
    title_ar: str | None = None

    cover_url: str | None = None

    class Config:
        from_attributes = True


class SearchAuthorResponse(BaseModel):
    id: UUID

    name_bn: str
    name_en: str | None = None
    name_ar: str | None = None

    class Config:
        from_attributes = True


class SearchPublisherResponse(BaseModel):
    id: UUID

    name_bn: str
    name_en: str | None = None
    name_ar: str | None = None

    class Config:
        from_attributes = True


class SearchTagResponse(BaseModel):
    id: UUID

    name: str

    class Config:
        from_attributes = True


class GlobalSearchResponse(BaseModel):
    books: list[SearchBookResponse]
    authors: list[SearchAuthorResponse]
    publishers: list[SearchPublisherResponse]
    tags: list[SearchTagResponse]
