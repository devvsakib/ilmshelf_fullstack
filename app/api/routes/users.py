from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import user_service
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.public_profile_schema import PublicProfileResponse
from app.schemas.user import UserResponse, UpdateProfileRequest, ChangePasswordRequest

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return user_service.get_me(current_user)


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.update_me(current_user, payload, db)


@router.patch("/me/password")
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.change_password(current_user, payload, db)


@router.get("/{user_id}", response_model=PublicProfileResponse)
def get_public_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = user_service.get_public_profile(user_id, db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user
