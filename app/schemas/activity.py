from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.activity import ActivityActionEnum

class ActivityResponse(BaseModel):
    id: UUID
    action: ActivityActionEnum
    entity_type: str
    entity_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True