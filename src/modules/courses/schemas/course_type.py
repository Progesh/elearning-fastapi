from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.core.enums import Status as CourseTypeStatus

_ALLOWED_STATUSES = (CourseTypeStatus.ACTIVE, CourseTypeStatus.INACTIVE)


class CourseTypeBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    status: CourseTypeStatus = Field(default=CourseTypeStatus.ACTIVE)


class CourseTypeCreate(CourseTypeBase):
    pass


class CourseTypeUpdate(CourseTypeBase):
    @field_validator("status")
    @classmethod
    def validate_status(cls, value: CourseTypeStatus) -> CourseTypeStatus:
        if value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class CourseTypeResponse(CourseTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
