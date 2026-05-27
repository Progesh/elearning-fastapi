from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.courses.models.course import Course
from src.modules.courses.models.course_type import CourseType
from src.modules.courses.schemas.course import CourseCreate, CourseUpdate
from src.core.pagination import paginate
from src.core.enums import Status as CourseStatus
from src.core.exceptions import UnprocessableEntityException, NotFoundException


class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def _get_active_course(self, course_id: int) -> Course:
        course = self.db.scalar(
            select(Course)
            .where(Course.id == course_id)
            .where(Course.status != CourseStatus.DELETED)
        )
        if not course:
            raise NotFoundException("Course not found")
        return course

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

    def get_by_id(self, course_id: int) -> Course:
        return self._get_active_course(course_id)

    def create(self, course_data: CourseCreate) -> Course:
        self._ensure_active_course_type(course_data.course_type_id)

        course = Course(**course_data.model_dump())
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)

        return course

    def update(self, course_id: int, course_data: CourseUpdate) -> Course:
        self._ensure_active_course_type(course_data.course_type_id)
        course = self._get_active_course(course_id)

        for key, value in course_data.model_dump().items():
            setattr(course, key, value)

        self.db.commit()
        self.db.refresh(course)
        return course

    def delete(self, course_id: int):
        course = self._get_active_course(course_id)
        course.status = CourseStatus.DELETED
        self.db.commit()
