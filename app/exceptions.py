class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


class DuplicateException(AppException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=409)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404)
