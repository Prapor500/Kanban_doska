from pydantic import BaseModel
from typing import Optional


class ProjectBase(BaseModel):
    created_by: int
    name:       str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    created_by: Optional[int] = None
    name:       Optional[str] = None


class ProjectOut(ProjectBase):
    id: int

    model_config = {"from_attributes": True}
