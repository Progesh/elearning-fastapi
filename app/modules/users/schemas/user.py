from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.modules.users.enums import UserStatus

_ALLOWED_STATUSES = (UserStatus.ACTIVE, UserStatus.INACTIVE)


class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    status: UserStatus = Field(default=UserStatus.ACTIVE)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: UserStatus) -> UserStatus:
        if value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class UserPatch(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    status: UserStatus | None = Field(default=None)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: UserStatus | None) -> UserStatus | None:
        if value is not None and value not in _ALLOWED_STATUSES:
            raise ValueError("Status must be active or inactive")
        return value


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
