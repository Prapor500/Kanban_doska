from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.infrastructure.jaminstance import jam
from src.core.services.db import get_db
from src.models.user import User
from typing import Optional

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


class RegisterRequest(BaseModel):
    email: str
    password: str


@auth.post("/register/init")
async def register_init(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    # Проверка существования пользователя
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(400, "Email already registered")

    # Создаем пользователя только
    user = User(
        email=request.email,
        password=request.password
    )

    db.add(user)
    db.commit()

    return {
        "message": "Аккаунт создан!",
        "user_id": user.id
    }


class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None


@auth.patch("/profile/{user_id}")
async def update_profile(
    user_id: int,
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    if request.first_name is not None:
        user.first_name = request.first_name
    if request.last_name is not None:
        user.last_name = request.last_name
    if request.middle_name is not None:
        user.middle_name = request.middle_name
    if request.gender is not None:
        user.gender = request.gender

    db.commit()
    return {"message": "Профиль обновлен"}
