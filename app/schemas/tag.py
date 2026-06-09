from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True
