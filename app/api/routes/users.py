from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services import user_service

from app.schemas.public_profile_schema import (
    PublicProfileResponse,
)

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=PublicProfileResponse,
)
def get_public_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = user_service.get_public_profile(
        user_id,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
