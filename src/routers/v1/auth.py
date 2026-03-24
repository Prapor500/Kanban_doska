from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.jaminstance import jam
from src.core.services.db import get_db
from src.models.user import User
from src.schemas.auth import LoginRequest, RegisterRequest
from src.core.services.auth_for_users import validate_user
from src.crud.users import create_user_raw

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login", status_code=status.HTTP_200_OK)
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


@auth.post("/register")
async def register_init(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    # Проверка существования пользователя
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(400, "Почта уже зарегистрирована")

    user = create_user_raw(db, email=request.email, password=request.password)
    return {"status": "ok"}
