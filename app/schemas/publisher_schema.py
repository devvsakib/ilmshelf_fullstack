from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PublisherCreate(BaseModel):
    name: str
    website: str | None = None


class PublisherUpdate(BaseModel):
    name: str | None = None
    website: str | None = None


class PublisherResponse(BaseModel):
    id: UUID
    name: str
    website: str | None
    created_at: datetime

    class Config:
        from_attributes = True
