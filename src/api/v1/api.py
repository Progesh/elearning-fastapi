from fastapi import APIRouter
from src.api.v1.routes.auth import router as auth_router
from src.api.v1.routes.celery_test import router as celery_test_router
from src.api.v1.routes.organizations import router as organizations_router
from src.api.v1.routes.users import router as users_router
from src.api.v1.routes.course_types import router as course_types_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    organizations_router, prefix="/organizations", tags=["organizations"]
)
api_router.include_router(
    course_types_router, prefix="/course_types", tags=["course_types"]
)
api_router.include_router(celery_test_router, prefix="/celery", tags=["celery-test"])
