from fastapi import APIRouter, Depends, Query, status

from src.modules.courses.services.course import CourseService
from src.core.database import DbSession
from src.core.dependencies import require_auth
from src.core.schemas import SingleResponse, PaginatedResponse
from src.modules.courses.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
)

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/", response_model=PaginatedResponse[CourseResponse])
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return CourseService(db).get_all(page, page_size)


@router.get("/{course_id}", response_model=SingleResponse[CourseResponse])
def show(course_id: int, db: DbSession):
    return SingleResponse(data=CourseService(db).get_by_id(course_id))


@router.post(
    "/",
    response_model=SingleResponse[CourseResponse],
    status_code=status.HTTP_201_CREATED,
)
def store(course_data: CourseCreate, db: DbSession):
    return SingleResponse(data=CourseService(db).create(course_data))


@router.put("/{course_id}", response_model=SingleResponse[CourseResponse])
def update(course_id: int, course_data: CourseUpdate, db: DbSession):
    return SingleResponse(data=CourseService(db).update(course_id, course_data))


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(course_id: int, db: DbSession):
    CourseService(db).delete(course_id)
