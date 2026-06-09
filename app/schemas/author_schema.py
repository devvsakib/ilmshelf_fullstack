from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name_bn: str
    name_en: str | None = None
    name_ar: str | None = None
    bio: str | None = None


class AuthorUpdate(BaseModel):
    name_bn: str | None = None
    name_en: str | None = None
    name_ar: str | None = None
    bio: str | None = None


class AuthorResponse(BaseModel):
    id: UUID
    name_bn: str
    name_en: str | None
    name_ar: str | None
    bio: str | None
    created_at: datetime

    class Config:
        from_attributes = True
