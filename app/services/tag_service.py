from sqlalchemy.orm import Session

from app.models.tag import Tag

from app.schemas.tag import TagCreate

from app.utils.slug import generate_slug


def create_tag(payload: TagCreate, db: Session):
    tag = Tag(
        name=payload.name,
        slug=generate_slug(payload.name),
    )

    db.add(tag)

    db.commit()

    db.refresh(tag)

    return tag


def get_tags(db: Session):
    return db.query(Tag).all()
