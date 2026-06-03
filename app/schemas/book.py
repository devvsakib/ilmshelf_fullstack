from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.enums import VisibilityEnum


class BookCreate(BaseModel):
    title_bn: str
    title_en: str | None = None
    title_ar: str | None = None

    description_bn: str | None = None
    description_en: str | None = None
    description_ar: str | None = None

    cover_url: str | None = None
    isbn: str | None = None
    pages: int | None = None
    price: float | None = None

    currency: str = "BDT"
    publisher_id: str | None = None
    published_year: str | None = None
    language: str | None = None
    visibility: VisibilityEnum
    book_metadata: dict | None = None


class BookResponse(BaseModel):
    id: UUID

    slug: str

    title_bn: str
    title_en: str | None = None
    title_ar: str | None = None

    description_bn: str | None = None
    description_en: str | None = None
    description_ar: str | None = None

    cover_url: str | None = None
    isbn: str | None = None
    pages: int | None = None
    price: float | None = None
    currency: str = "BDT"
    published_year: int | None = None
    language: str | None = None
    visibility: VisibilityEnum
    publisher_id: UUID | None = None
    owner_id: UUID | None = None
    created_at: datetime

    class Config:
        from_attributes = True
