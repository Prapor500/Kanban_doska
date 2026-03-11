from pydantic import BaseModel
from typing import Optional


class ExampleSchema(BaseModel):
    id: int
    text_data: Optional[str]
