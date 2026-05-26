from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.core.enums import Status as CourseStatus


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=CourseStatus.ACTIVE)
    course_type_id = Column(Integer, ForeignKey("course_type.id"), nullable=True)

    course_type = relationship("CourseType")
