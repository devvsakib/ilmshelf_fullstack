from sqlalchemy.orm import Session
from uuid import UUID
from app.models.activity import Activity, ActivityActionEnum


def log_activity(
    db: Session,
    user_id: UUID,
    action: ActivityActionEnum,
    entity_type: str,
    entity_id: UUID,
) -> Activity:
    activity = Activity(
        user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id
    )
    db.add(activity)
    return activity


def get_user_activities(db: Session, user_id: UUID, limit: int = 20):
    return (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
        .order_by(Activity.created_at.desc())
        .limit(limit)
        .all()
    )
