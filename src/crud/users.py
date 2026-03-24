from sqlalchemy.orm import Session
from src.models.user import User


def create_user_raw(db: Session, email: str, password: str) -> User:
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    return user
