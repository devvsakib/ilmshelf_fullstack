from app.db.database import SessionLocal

from app.models.user import User
from app.models.enums import UserRoleEnum

from app.core.security import hash_password

EMAIL = "admin@ilmshelf.com"
PASSWORD = "Admin123!"


def run():
    db = SessionLocal()

    exists = db.query(User).filter(User.email == EMAIL).first()

    if exists:
        print("Admin already exists")
        return

    admin = User(
        username="admin",
        email=EMAIL,
        full_name="System Admin",
        password_hash=hash_password(PASSWORD),
        role=UserRoleEnum.ADMIN,
    )

    db.add(admin)

    db.commit()

    print("Admin created successfully")


if __name__ == "__main__":
    run()
