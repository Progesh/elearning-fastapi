from fastapi import APIRouter, Query

from src.modules.courses.services.course import CourseService
from src.core.database import DbSession
from src.core.schemas import SingleResponse, PaginatedResponse
from src.modules.courses.schemas.course import CourseResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[CourseResponse])
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100)
):
    return CourseService(db).get_all(page, page_size)