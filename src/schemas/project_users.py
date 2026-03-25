from pydantic import BaseModel
from typing import Optional


class ProjectUserBase(BaseModel):
    user_id:    int
    project_id: int


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUserUpdate(BaseModel):
    user_id:    Optional[int] = None
    project_id: Optional[int] = None


class ProjectUserOut(ProjectUserBase):
    model_config = {"from_attributes": True}
