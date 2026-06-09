from datetime import datetime


def soft_delete(instance, db):
    instance.deleted_at = datetime.utcnow()

    db.commit()

    db.refresh(instance)

    return instance
