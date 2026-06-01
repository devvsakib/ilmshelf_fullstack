from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
import uuid
from app.models.enums import ShelfTypeEnum

class ShelfCreate(BaseModel):
    name: str
    slug: str
    type: ShelfTypeEnum
    is_public: bool = True
    created_by: uuid.UUID | None = None
