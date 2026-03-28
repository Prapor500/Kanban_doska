# src/routers/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.schemas.auth import LoginRequest, RegisterRequest
from src.core.services.auth_for_users import validate_user
from src.crud.users import create_user_raw, get_user_by_email
from src.infrastructure.jwt_backend import make_access_token

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login", status_code=status.HTTP_200_OK)
async def log_in(request: LoginRequest, db: Session = Depends(get_db)):
    if not validate_user(request.email, request.password, db):
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = make_access_token({"sub": request.email})
    return {"access_token": token, "token_type": "Bearer"}


@auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_email(db, request.email):
        raise HTTPException(400, "Почта уже зарегистрирована")

    user = create_user_raw(db, email=request.email, password=request.password)
    return {"status": "ok", "user_id": user.id}
