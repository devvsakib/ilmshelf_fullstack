from sqlalchemy.orm import Session
from app.models.user import User
from app.models.reading_goal import ReadingGoal
from app.schemas.reading_goal import ReadingGoalCreate, ReadingGoalUpdate


def create_reading_goal(
    payload: ReadingGoalCreate,
    current_user: User,
    db: Session,
):
    existing = (
        db.query(ReadingGoal)
        .filter(
            ReadingGoal.user_id == current_user.id,
            ReadingGoal.year == payload.year,
        )
        .first()
    )

    if existing:
        raise ValueError("Goal with same year already exists")

    goal = ReadingGoal(
        user_id=current_user.id,
        year=payload.year,
        target_books=payload.target_books,
    )

    db.add(goal)

    db.commit()

    db.refresh(goal)

    return goal


def get_reading_goals(current_user: User, db: Session):
    return db.query(ReadingGoal).filter(ReadingGoal.user_id == current_user.id).all()


def update_reading_goals(
    reading_goal_id, payload: ReadingGoalUpdate, current_user: User, db: Session
):
    reading_goals = (
        db.query(ReadingGoal)
        .filter(
            ReadingGoal.id == reading_goal_id, ReadingGoal.user_id == current_user.id
        )
        .first()
    )
    if not reading_goals:
        raise ValueError("No goal exist")

    if payload.target_books is not None:
        reading_goals.target_books = payload.target_books

    if payload.completed_books is not None:
        reading_goals.completed_books = payload.completed_books

    db.commit()
    db.refresh(reading_goals)

    return reading_goals


def delete_reading_goal(
    reading_goal_id,
    current_user: User,
    db: Session,
):
    remove_goal = (
        db.query(ReadingGoal)
        .filter(
            ReadingGoal.id == reading_goal_id, ReadingGoal.user_id == current_user.id
        )
        .first()
    )

    if not remove_goal:
        raise ValueError("Goal not found")

    db.delete(remove_goal)

    db.commit()

    return True
