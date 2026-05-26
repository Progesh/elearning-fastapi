from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.modules.courses.models.course import Course
from src.core.pagination import paginate
from src.core.enums import Status as CourseStatus
from src.core.exceptions import NotFoundException


class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, page: int = 1, page_size: int = 20) -> dict:
        courses = select(Course).where(Course.status == CourseStatus.ACTIVE)
        return paginate(self.db, courses, page, page_size)
