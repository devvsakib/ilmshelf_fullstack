from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.core.dependencies import get_current_user

from app.schemas.book import (
    BookCreate,
    BookResponse,
)

from app.services.book_service import (
    create_book,
    get_books,
    get_book,
)

router = APIRouter()


@router.post(
    "",
    response_model=BookResponse,
)
def create_new_book(
    payload: BookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_book(
            payload,
            current_user,
            db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[BookResponse],
)
def list_books(
    db: Session = Depends(get_db),
):
    return get_books(db)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
)
def get_single_book(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    book = get_book(
        book_id,
        db,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book
