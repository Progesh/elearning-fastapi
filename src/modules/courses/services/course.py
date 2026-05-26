from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.courses.models.course import Course
from src.modules.courses.models.course_type import CourseType
from src.modules.courses.schemas.course import CourseCreate
from src.core.pagination import paginate
from src.core.enums import Status as CourseStatus
from src.core.exceptions import UnprocessableEntityException


class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def _ensure_active_course_type(self, course_type_id: int) -> None:
        active_course_type = self.db.scalar(
            select(CourseType)
            .where(CourseType.id == course_type_id)
            .where(CourseType.status == CourseStatus.ACTIVE)
        )

        if not active_course_type:
            raise UnprocessableEntityException.validation_error(
                field="course_type_id",
                message="course_type_id must reference an active course type",
            )

    def get_all(self, page: int = 1, page_size: int = 20) -> dict:
        courses = select(Course).where(Course.status == CourseStatus.ACTIVE)
        return paginate(self.db, courses, page, page_size)

    def create(self, course_data: CourseCreate) -> Course:
        self._ensure_active_course_type(course_data.course_type_id)

        course = Course(**course_data.model_dump())
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)

        return course
