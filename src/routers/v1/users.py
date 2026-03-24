from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.models.user import User
from src.schemas.users import ProfileUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/profile/{user_id}")
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
