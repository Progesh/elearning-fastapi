from fastapi import APIRouter, Query

from src.core.database import DbSession

router = APIRouter()

@router.get("/")
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100)
):
    return {"test": "test"}