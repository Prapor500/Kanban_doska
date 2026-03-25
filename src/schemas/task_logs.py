from pydantic import BaseModel
from typing import Optional
import datetime


class TaskLogBase(BaseModel):
    task_id: int
    message: str


class TaskLogCreate(TaskLogBase):
    pass


class TaskLogUpdate(BaseModel):
    message: Optional[str] = None


class TaskLogOut(TaskLogBase):
    id: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
