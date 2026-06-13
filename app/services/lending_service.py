from datetime import datetime

from app.models.lending_record import (
    LendingRecord,
)

from app.schemas.lending_record_schema import (
    LendingRecordCreate,
)


def lend_book(
    payload: LendingRecordCreate,
    current_user,
    db,
):
    item = LendingRecord(
        user_id=current_user.id,
        book_id=payload.book_id,
        borrower_name=payload.borrower_name,
        borrower_phone=payload.borrower_phone,
        due_date=payload.due_date,
    )

    db.add(item)

    db.commit()
    db.refresh(item)

    return item


def my_lent_books(
    user_id,
    db,
):
    return (
        db.query(LendingRecord)
        .filter(
            LendingRecord.user_id == user_id,
            LendingRecord.returned_at.is_(None),
        )
        .all()
    )


def mark_returned(
    lending_id,
    user_id,
    db,
):
    item = (
        db.query(LendingRecord)
        .filter(
            LendingRecord.id == lending_id,
            LendingRecord.user_id == user_id,
        )
        .first()
    )

    if not item:
        return None

    item.returned_at = datetime.utcnow()

    db.commit()
    db.refresh(item)

    return item
