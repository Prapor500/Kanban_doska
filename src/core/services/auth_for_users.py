from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.models.user import User
from src.infrastructure.jwt_backend import verify_token
from src.crud.users import get_user_by_email
from src.core.services.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def validate_user(email: str, password: str, db: Session) -> bool:  # Проверка пользователя
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"DEBUG: User with email {email} not found")
        return False
    
    is_valid = user.password == password
    if not is_valid:
        print(f"DEBUG: Password mismatch for {email}")
        print(f"DEBUG: Input:  '{password}' (len: {len(password)})")
        print(f"DEBUG: Stored: '{user.password}' (len: {len(user.password)})")
    
    return is_valid

def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
