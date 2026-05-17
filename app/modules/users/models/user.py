from sqlalchemy import Column, Integer, String

from app.core.database import Base
from app.core.enums import Status as UserStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default=UserStatus.ACTIVE)
