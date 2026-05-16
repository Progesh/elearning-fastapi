from fastapi import APIRouter, status

from app.core.database import DbSession
from app.modules.users.schemas.user import (
    UserCreate,
    UserPatch,
    UserUpdate,
    UserResponse,
)
from app.modules.users.services.user import UserService

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def index(db: DbSession):
    return UserService(db).get_all()


@router.get("/{user_id}", response_model=UserResponse)
def show(user_id: int, db: DbSession):
    return UserService(db).get_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def store(user_data: UserCreate, db: DbSession):
    return UserService(db).create(user_data)


@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, user_data: UserUpdate, db: DbSession):
    return UserService(db).update(user_id, user_data)


@router.patch("/{user_id}", response_model=UserResponse)
def partial_update(user_id: int, user_data: UserPatch, db: DbSession):
    return UserService(db).partial_update(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(user_id: int, db: DbSession):
    UserService(db).delete(user_id)
