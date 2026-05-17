from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import Status as OrganizationStatus

_ALLOWED_STATUSES = (OrganizationStatus.ACTIVE, OrganizationStatus.INACTIVE)


class OrganizationBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    status: OrganizationStatus = Field(default=OrganizationStatus.ACTIVE)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    @field_validator("status")
    @classmethod
    def validate_status(cls, value: OrganizationStatus) -> OrganizationStatus:
        if value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class OrganizationPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    status: OrganizationStatus | None = Field(default=None)

    @field_validator("status")
    @classmethod
    def validate_status(
        cls, value: OrganizationStatus | None
    ) -> OrganizationStatus | None:
        if value is not None and value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class OrganizationResponse(OrganizationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
