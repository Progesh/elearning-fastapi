from fastapi import APIRouter, Query, status

from app.core.database import DbSession
from app.core.schemas import PaginatedResponse, SingleResponse
from app.modules.users.schemas.user import (
    UserCreate,
    UserPatch,
    UserUpdate,
    UserResponse,
)
from app.modules.users.services.user import UserService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[UserResponse])
def index(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return UserService(db).get_all(page=page, page_size=page_size)


@router.get("/{user_id}", response_model=SingleResponse[UserResponse])
def show(user_id: int, db: DbSession):
    return SingleResponse(data=UserService(db).get_by_id(user_id))


@router.post("/", response_model=SingleResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def store(user_data: UserCreate, db: DbSession):
    return SingleResponse(data=UserService(db).create(user_data))


@router.put("/{user_id}", response_model=SingleResponse[UserResponse])
def update(user_id: int, user_data: UserUpdate, db: DbSession):
    return SingleResponse(data=UserService(db).update(user_id, user_data))


@router.patch("/{user_id}", response_model=SingleResponse[UserResponse])
def partial_update(user_id: int, user_data: UserPatch, db: DbSession):
    return SingleResponse(data=UserService(db).partial_update(user_id, user_data))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: DbSession):
    UserService(db).delete(user_id)
