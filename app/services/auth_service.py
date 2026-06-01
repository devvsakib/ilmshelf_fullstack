from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, create_access_token, verify_password


def create_user(payload: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise ValueError("Email Already Exists!")

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }