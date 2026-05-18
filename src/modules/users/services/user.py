from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.pagination import paginate
from src.core.exceptions import DuplicateException, NotFoundException
from src.core.enums import Status as UserStatus
from src.modules.users.models.user import User
from src.modules.users.schemas.user import UserCreate, UserPatch, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def _get_active_user(self, user_id: int) -> User:
        user = self.db.scalar(
            select(User)
            .where(User.id == user_id)
            .where(User.status != UserStatus.DELETED)
        )
        if not user:
            raise NotFoundException("User not found")
        return user

    def create(self, user_data: UserCreate) -> User:
        existing = self.db.scalar(select(User).where(User.email == user_data.email))
        if existing:
            raise DuplicateException("User with this email already exists")

        user = User(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = self._get_active_user(user_id)

        for key, value in user_data.model_dump().items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def partial_update(self, user_id: int, user_data: UserPatch) -> User:
        user = self._get_active_user(user_id)

        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def get_all(self, page: int = 1, page_size: int = 20) -> dict:
        query = select(User).where(User.status == UserStatus.ACTIVE)
        return paginate(self.db, query, page, page_size)

    def get_by_id(self, user_id: int) -> User:
        return self._get_active_user(user_id)

    def delete(self, user_id: int) -> None:
        user = self._get_active_user(user_id)
        user.status = UserStatus.DELETED
        self.db.commit()
