from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.core.enums import Status as CourseStatus

_ALLOWED_STATUSES = (CourseStatus.ACTIVE, CourseStatus.INACTIVE)


class CourseBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    status: CourseStatus = Field(default=CourseStatus.ACTIVE)
    course_type_id: int = Field(ge=1)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    @field_validator("status")
    @classmethod
    def validate_status(cls, value: CourseStatus) -> CourseStatus:
        if value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
