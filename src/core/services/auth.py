from .db import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi import Depends, HTTPException, Request
from src.infrastructure.jaminstance import jam
from jam.exceptions import TokenLifeTimeExpired
from models.user import User


def get_access_token(user_id):
    payload = jam.make_payload(exp=600, **{"user_id": user_id})
    token = jam.gen_jwt_token(payload)
    return token


def get_refresh_token(user_id):
    payload = jam.make_payload(**{"user_id": user_id})
    token = jam.gen_jwt_token(payload)
    return token


def get_check_token(token):
    try:
        jam.verify_jwt_token(
            token=token,
            check_exp=True,
            check_list=False
        )
    except TokenLifeTimeExpired:
        return False
    except ValueError:
        return False
    return True


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    # Берём токен
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]

    # Если токена нет — ошибка
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена")

    # Декодируем токен (пусть падает, если невалидный)
    user_id = jam.verify_jwt_token(token)["user_id"]

    # Ищем юзера
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Юзер не найден")

    return user
