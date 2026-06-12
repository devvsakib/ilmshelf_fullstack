from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.models.enums import RoleEnum


class AdminUserResponse(BaseModel):
    id: UUID

    username: str
    email: str
    full_name: str

    role: RoleEnum
    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True


class UpdateUserRoleRequest(BaseModel):
    role: RoleEnum
