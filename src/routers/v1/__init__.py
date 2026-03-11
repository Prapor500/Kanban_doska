from fastapi import APIRouter
from .example import router as example_router


router = APIRouter()
router.include_router(example_router, prefix="/example_tag", tags=["Examples"])
