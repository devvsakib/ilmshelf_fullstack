from sqlalchemy.orm import Session

from app.models.publisher import Publisher
from app.schemas.publisher import PublisherCreate


def create_publisher(payload: PublisherCreate, db: Session):
    publisher = Publisher(
        name=payload.name,
        website=payload.website,
    )

    db.add(publisher)

    db.commit()

    db.refresh(publisher)

    return publisher


def get_publishers(db: Session):
    return db.query(Publisher).all()
