from uuid import UUID
from pydantic import BaseModel


class DiscoverBookResponse(BaseModel):
    id: UUID

    title_bn: str | None = None
    title_en: str | None = None

    cover_url: str | None = None

    class Config:
        from_attributes = True
