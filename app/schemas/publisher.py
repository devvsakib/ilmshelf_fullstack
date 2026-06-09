from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class PublisherCreate(BaseModel):
    name = str
    website = str


class PublishUpdate(BaseModel):
    name = str
    website = str | None = None


class PublisherResponse(BaseModel):
    name = str
    website = str | None = None
    

class PublisherResponse(BaseModel):
    id: UUID
    name: str
    website: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True
