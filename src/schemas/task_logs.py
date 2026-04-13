from pydantic import BaseModel
from typing import Optional
import datetime
from src.schemas.users import UserOut


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
    user_id: Optional[int] = None
    user: Optional[UserOut] = None

    model_config = {"from_attributes": True}
