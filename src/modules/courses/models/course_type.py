from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.core.enums import Status as CourseTypeStatus


class CourseType(Base):
    __tablename__ = "course_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), default=CourseTypeStatus.ACTIVE)

    courses = relationship("Course", back_populates="course_type")
