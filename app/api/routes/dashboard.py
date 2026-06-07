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

from app.services.dashboard_service import get_dashboard

router = APIRouter()

@router.get(
    "",
    # response_model=list[BookResponse],
)
def user_dashbaord(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_dashboard(current_user, db)
