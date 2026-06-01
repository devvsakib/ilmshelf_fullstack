from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class PublisherCreate(BaseModel):
    name = str
    website = str


class PublishUpdate(BaseModel):
    name = str
    website = str


class PublisherResponse(BaseModel):
    name = str
    website = str
