from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.modules.courses.schemas.course_type import CourseTypeCreate, CourseTypeUpdate
from src.modules.courses.models.course_type import CourseType
from src.core.pagination import paginate
from src.core.enums import Status as CourseTypeStatus
from src.core.exceptions import NotFoundException


class CourseTypeService:
    def __init__(self, db: Session):
        self.db = db

    def _get_active_course_type(self, course_type_id: int):
        course_type = self.db.scalar(
            select(CourseType)
            .where(CourseType.id == course_type_id)
            .where(CourseType.status != CourseTypeStatus.DELETED)
        )
        if not course_type:
            raise NotFoundException("Course type id not found")

        return course_type

    def get_all(self, page: int = 1, page_size: int = 20) -> dict:
        query = select(CourseType).where(CourseType.status == CourseTypeStatus.ACTIVE)
        return paginate(self.db, query, page, page_size)

    def get_by_id(self, course_type_id: int) -> CourseType:
        return self._get_active_course_type(course_type_id)

    def create(self, course_type_data: CourseTypeCreate) -> CourseType:
        course_type = CourseType(**course_type_data.model_dump())
        self.db.add(course_type)
        self.db.commit()
        self.db.refresh(course_type)

        return course_type

    def update(
        self, course_type_id: int, course_type_data: CourseTypeUpdate
    ) -> CourseType:
        course_type = self._get_active_course_type(course_type_id)

        self.db.execute(
            update(CourseType)
            .where(CourseType.id == course_type_id)
            .values(**course_type_data.model_dump())
        )
        self.db.commit()
        self.db.refresh(course_type)

        return course_type

    def delete(self, course_type_id: int):
        course_type = self._get_active_course_type(course_type_id)
        course_type.status = CourseTypeStatus.DELETED
        self.db.commit()
