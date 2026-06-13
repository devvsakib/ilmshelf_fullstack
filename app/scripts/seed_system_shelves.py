from app.db.database import SessionLocal

from app.models.shelf import Shelf
from app.models.enums import ShelfTypeEnum

SYSTEM_SHELVES = [
    {
        "name": "Want To Read",
        "type": ShelfTypeEnum.SYSTEM,
    },
    {
        "name": "Reading",
        "type": ShelfTypeEnum.SYSTEM,
    },
    {
        "name": "Completed",
        "type": ShelfTypeEnum.SYSTEM,
    },
    {
        "name": "On Hold",
        "type": ShelfTypeEnum.SYSTEM,
    },
    {
        "name": "Dropped",
        "type": ShelfTypeEnum.SYSTEM,
    },
]


def run():
    db = SessionLocal()

    for shelf_data in SYSTEM_SHELVES:
        exists = (
            db.query(Shelf)
            .filter(
                Shelf.name == shelf_data["name"],
                Shelf.type == ShelfTypeEnum.SYSTEM,
            )
            .first()
        )

        if exists:
            continue

        shelf = Shelf(
            name=shelf_data["name"],
            type=shelf_data["type"],
        )

        db.add(shelf)

    db.commit()

    print("System shelves seeded successfully")


if __name__ == "__main__":
    run()
