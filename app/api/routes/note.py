from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.core.dependencies import (
    get_current_user,
)

from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
)

from app.services.note_service import (
    create_note,
    get_notes,
    # update_note,
    # delete_note,
)

router = APIRouter()


@router.post(
    "",
    response_model=NoteResponse,
)
def create_new_note(
    payload: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_note(
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
    response_model=list[NoteResponse],
)
def list_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_notes(
        current_user,
        db,
    )
