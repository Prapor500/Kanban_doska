from pydantic import BaseModel
from typing import Optional


class ProjectUserBase(BaseModel):
    project_id: int
    user_id:    int
    role:       Optional[str] = 'viewer'


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUserUpdate(BaseModel):
    role: Optional[str] = None


class ProjectUserOut(ProjectUserBase):
    id: int

    model_config = {"from_attributes": True}
