from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.schemas.user_book import UserBookCreate, UserBookResponse, UserBookUpdate
from app.services.user_book_service import (
    create_user_book,
    get_my_library,
    update_user_book,
)

router = APIRouter()


@router.post("/", response_model=UserBookResponse)
def add_book_to_library(
    payload: UserBookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_user_book(payload, current_user, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/my-library", response_model=list[UserBookResponse])
def my_library(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_my_library(current_user, db)


@router.patch("/{user_book_id}", response_model=UserBookResponse)
def update_library_book(
    user_book_id: UUID,
    payload: UserBookUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_user_book(
            user_book_id,
            payload,
            current_user,
            db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
