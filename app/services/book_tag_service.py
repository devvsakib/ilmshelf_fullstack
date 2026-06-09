from app.models.book_tag import BookTag
from app.models.tag import Tag


def assign_tag(
    book_id,
    payload,
    db,
):
    tag = (
        db.query(Tag)
        .filter(
            Tag.id == payload.tag_id
        )
        .first()
    )

    if not tag:
        raise ValueError(
            "Tag not found"
        )

    relation = BookTag(
        book_id=book_id,
        tag_id=payload.tag_id,
    )

    db.add(relation)

    db.commit()

    db.refresh(relation)

    return relation