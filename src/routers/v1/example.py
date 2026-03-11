from fastapi import APIRouter
from typing import Optional
from schemas.example import ExampleSchema

router = APIRouter()


@router.post("/example",
             response_model=ExampleSchema)
async def example_endpoint(some_id: int,
                           some_text_data: Optional[str] = "Base text data"):
    return ExampleSchema(id=some_id,
                         text_data=some_text_data)
