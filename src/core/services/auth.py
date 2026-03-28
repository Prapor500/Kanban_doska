from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from src.infrastructure.jwt_backend import make_access_token, verify_token
from src.core.services.db import get_db
from src.models.user import User


def get_access_token(user_id: int, *, exp: Optional[int] = 600) -> str:
    payload: Dict[str, Any] = {"user_id": user_id}
    return make_access_token(payload, exp=exp)


def get_refresh_token(user_id: int) -> str:
    payload: Dict[str, Any] = {"user_id": user_id}
    return make_access_token(payload)  # без exp — возьмёт default из settings


def get_check_token(token: str) -> bool:
    try:
        _ = verify_token(token, check_exp=True)
        return True
    except Exception:
        return False


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    # Берём Bearer-токен
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split("Bearer ")[-1].strip() if auth_header else ""
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена")

    try:
        payload = verify_token(token, check_exp=True)
    except Exception:
        raise HTTPException(
            status_code=401, detail="Невалидный или просроченный токен")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="В токене нет user_id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Юзер не найден")

    return user
