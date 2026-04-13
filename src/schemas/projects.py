from pydantic import BaseModel, EmailStr
from typing import Optional


class UserInProject(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ProjectBase(BaseModel):
    created_by: int
    name:       str


class ProjectCreate(ProjectBase):
    columns: Optional[list[str]] = None
    member_emails: Optional[list[EmailStr]] = None


class ProjectUpdate(BaseModel):
    created_by: Optional[int] = None
    name:       Optional[str] = None


class ProjectOut(ProjectBase):
    id: int
    users: list[UserInProject] = []
    creator: UserInProject

    model_config = {"from_attributes": True}
