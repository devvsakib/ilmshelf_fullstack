from datetime import datetime
from sqlalchemy.orm import Session

from app.models.publisher import Publisher
from app.schemas.publisher_schema import PublisherCreate, PublisherUpdate


def create_publisher(
    payload: PublisherCreate,
    db: Session,
):
    publisher = Publisher(**payload.model_dump())

    db.add(publisher)
    db.commit()
    db.refresh(publisher)

    return publisher


def get_publishers(
    db: Session,
):
    return (
        db.query(Publisher)
        .filter(Publisher.deleted_at.is_(None))
        .order_by(Publisher.name)
        .all()
    )


def get_publisher(
    publisher_id,
    db: Session,
):
    return (
        db.query(Publisher)
        .filter(
            Publisher.id == publisher_id,
            Publisher.deleted_at.is_(None),
        )
        .first()
    )


def update_publisher(
    publisher_id,
    payload: PublisherUpdate,
    db: Session,
):
    publisher = get_publisher(
        publisher_id,
        db,
    )

    if not publisher:
        return None

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(
            publisher,
            key,
            value,
        )

    db.commit()
    db.refresh(publisher)

    return publisher


def delete_publisher(
    publisher_id,
    db: Session,
):
    publisher = get_publisher(
        publisher_id,
        db,
    )

    if not publisher:
        return None

    publisher.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Publisher deleted successfully"}
