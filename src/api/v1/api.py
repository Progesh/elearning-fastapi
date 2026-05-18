from fastapi import APIRouter
from src.api.v1.routes.users import router as users_router
from src.api.v1.routes.organizations import router as organizations_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    organizations_router, prefix="/organizations", tags=["organizations"]
)
