from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.infrastructure.jaminstance import jam
from core.services.db import get_db
from models.user import User

auth = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


def validate_user(email: str, password: str, db: Session) -> bool:  # Проверка пользователя
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    return user.password == password


@auth.post("/login")
async def log_in(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    if not validate_user(request.email, request.password, db):
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # токен с email в payload
    token = jam.gen_jwt_token({"sub": request.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
