from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.activity import ActivityResponse
from app.services.activity_service import get_user_activities

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("", response_model=List[ActivityResponse])
def fetch_my_activity_feed(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_activities(db=db, user_id=current_user.id, limit=limit)
