from fastapi import APIRouter, Depends, Query, status

from src.modules.courses.schemas.course_type import (
    CourseTypeResponse,
    CourseTypeCreate,
    CourseTypeUpdate,
)
from src.modules.courses.services.course_type import CourseTypeService
from src.core.dependencies import require_auth
from src.core.database import DbSession
from src.core.schemas import SingleResponse, PaginatedResponse

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/", response_model=PaginatedResponse[CourseTypeResponse])
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return CourseTypeService(db).get_all(page, page_size)


@router.get("/{course_type_id}", response_model=SingleResponse[CourseTypeResponse])
def show(course_type_id: int, db: DbSession):
    return SingleResponse(data=CourseTypeService(db).get_by_id(course_type_id))


@router.post(
    "/",
    response_model=SingleResponse[CourseTypeResponse],
    status_code=status.HTTP_201_CREATED,
)
def store(course_type_data: CourseTypeCreate, db: DbSession):
    return SingleResponse(data=CourseTypeService(db).create(course_type_data))


@router.put("/{course_type_id}", response_model=SingleResponse[CourseTypeResponse])
def update(course_type_id: int, course_type_data: CourseTypeUpdate, db: DbSession):
    return SingleResponse(
        data=CourseTypeService(db).update(course_type_id, course_type_data)
    )


@router.delete("/{course_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(course_type_id: int, db: DbSession):
    CourseTypeService(db).delete(course_type_id)
