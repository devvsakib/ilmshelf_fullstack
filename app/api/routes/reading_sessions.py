from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.auth import get_current_user

from app.services import (
    reading_session_service,
)

from app.schemas.reading_session_schema import (
    ReadingSessionCreate,
    ReadingSessionResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ReadingSessionResponse,
)
def create_session(
    payload: ReadingSessionCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = reading_session_service.create_session(
        payload,
        current_user.id,
        db,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return result


@router.get(
    "/my",
    response_model=list[ReadingSessionResponse],
)
def get_my_sessions(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return reading_session_service.get_my_sessions(
        current_user.id,
        db,
    )
