from typing import Any


class AppException(Exception):
    def __init__(self, detail: Any, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


class DuplicateException(AppException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=409)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404)


class UnprocessableEntityException(AppException):
    def __init__(self, detail: Any = "Validation failed"):
        super().__init__(detail=detail, status_code=422)

    @classmethod
    def validation_error(
        cls,
        *,
        field: str,
        message: str,
        location: str = "body",
        error_type: str = "value_error",
    ) -> "UnprocessableEntityException":
        return cls(
            [
                {
                    "loc": [location, field],
                    "msg": message,
                    "type": error_type,
                }
            ]
        )
