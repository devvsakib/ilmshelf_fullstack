from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.schemas.reading_goal import (
    ReadingGoalCreate,
    ReadingGoalResponse,
    ReadingGoalUpdate,
)

from app.services.reading_goals_service import (
    create_reading_goal,
    get_reading_goals,
    update_reading_goals,
    delete_reading_goal
)

router = APIRouter()


@router.post("", response_model=ReadingGoalResponse)
def new_reading_goals(
    payload: ReadingGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_reading_goal(payload, current_user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[ReadingGoalResponse])
def new_reading_goals(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        return get_reading_goals(current_user, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{reading_goal_id}", response_model=ReadingGoalResponse)
def update_existing_reading_goals(
    reading_goal_id,
    payload: ReadingGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_reading_goals(reading_goal_id, payload, current_user, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reading_goal_id}")
def delete_existing_reading_goals(
    reading_goal_id,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return delete_reading_goal(reading_goal_id, current_user, db)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
