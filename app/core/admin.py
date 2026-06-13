from fastapi import Depends
from fastapi import HTTPException

from app.models.enums import RoleEnum

from app.core.auth import get_current_user


def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin only",
        )

    return current_user
