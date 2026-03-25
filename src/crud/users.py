from sqlalchemy.orm import Session
from src.models.user import User
from sqlalchemy.orm import Session
from src.schemas.users import UserUpdate


def create_user_raw(db: Session, email: str, password: str) -> User:
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, data: UserUpdate) -> User | None:
    obj = get_user(db, user_id)
    if not obj:
        return None
    for key, val in data.dict(exclude_unset=True).items():
        setattr(obj, key, val)
    db.commit()
    db.refresh(obj)
    return obj


def delete_user(db: Session, user_id: int) -> User | None:
    obj = get_user(db, user_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
