from pydantic import BaseModel
from typing import Optional


class ColumnBase(BaseModel):
    project_id: int
    name: str
    position: Optional[int] = 0


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None


class ColumnOut(ColumnBase):
    id: int

    model_config = {"from_attributes": True}
