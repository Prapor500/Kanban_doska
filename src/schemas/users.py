from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None


# for crud
class UserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    gender: Optional[str]
    email: Optional[EmailStr]


class UserOut(UserBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
