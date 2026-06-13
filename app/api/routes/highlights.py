from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.auth import get_current_user

from app.schemas.highlight import HighlightCreate, HighlightUpdate, HighlightResponse

from app.services.highlight_service import (
    create_highlight,
    get_highlights,
    update_highlight,
    delete_highlight,
)

router = APIRouter()


@router.post(
    "",
    response_model=HighlightResponse,
)
def create_new_highlight(
    payload: HighlightCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_highlight(
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
    response_model=list[HighlightResponse],
)
def list_highlights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_highlights(
        current_user,
        db,
    )


@router.patch(
    "/{highlight_id}",
    response_model=HighlightResponse,
)
def edit_highlight(
    highlight_id: UUID,
    payload: HighlightUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_highlight(
            highlight_id,
            payload,
            current_user,
            db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{highlight_id}",
)
def remove_highlight(
    highlight_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_highlight(
            highlight_id,
            current_user,
            db,
        )

        return {"message": "Highlight deleted"}

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
