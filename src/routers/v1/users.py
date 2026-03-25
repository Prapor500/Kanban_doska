from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.models.user import User
from src.schemas.users import ProfileUpdateRequest, UserOut, UserUpdate
from typing import List
from src.crud.users import get_users, get_user, update_user, delete_user

router_users = APIRouter(prefix="/users", tags=["users"])


@router_users.patch("/profile/{user_id}")
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


@router_users.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)


@router_users.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router_users.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, data)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router_users.delete("/{user_id}", response_model=UserOut)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
