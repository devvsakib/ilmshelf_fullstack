from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.auth import get_current_user

from app.schemas.lending_record_schema import (
    LendingRecordCreate,
    LendingRecordResponse,
)

from app.services import lending_service

router = APIRouter()


@router.post(
    "/",
    response_model=LendingRecordResponse,
)
def lend_book(
    payload: LendingRecordCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return lending_service.lend_book(
        payload,
        current_user,
        db,
    )


@router.get(
    "/my",
    response_model=list[LendingRecordResponse],
)
def my_lent_books(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return lending_service.my_lent_books(
        current_user.id,
        db,
    )


@router.patch(
    "/{lending_id}/return",
    response_model=LendingRecordResponse,
)
def return_book(
    lending_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = lending_service.mark_returned(
        lending_id,
        current_user.id,
        db,
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )

    return item
