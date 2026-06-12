from datetime import datetime
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag_schema import TagCreate, TagUpdate

from app.utils.slug import generate_slug


def create_tag(
    payload: TagCreate,
    db: Session,
):
    tag = Tag(
        name=payload.name,
        slug=generate_slug(payload.name),
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_tags(db: Session):
    return db.query(Tag).filter(Tag.deleted_at.is_(None)).order_by(Tag.name).all()


def get_tag(tag_id, db: Session):
    return (
        db.query(Tag)
        .filter(
            Tag.id == tag_id,
            Tag.deleted_at.is_(None),
        )
        .first()
    )


def update_tag(
    tag_id,
    payload: TagUpdate,
    db: Session,
):
    tag = get_tag(tag_id, db)

    if not tag:
        return None

    if payload.name:
        tag.name = payload.name
        tag.slug = generate_slug(payload.name)

    db.commit()
    db.refresh(tag)

    return tag


def delete_tag(
    tag_id,
    db: Session,
):
    tag = get_tag(tag_id, db)

    if not tag:
        return None

    tag.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Tag deleted successfully"}
