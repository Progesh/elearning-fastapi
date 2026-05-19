from datetime import datetime, timedelta, timezone

import jwt

from src.core.config import Settings


def create_access_token(settings: Settings) -> tuple[str, int]:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRY_MINUTES
    )
    payload = {
        "sub": settings.API_CLIENT_ID,
        "exp": expires_at,
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    expires_in = settings.JWT_EXPIRY_MINUTES * 60
    return token, expires_in


def decode_access_token(token: str, settings: Settings) -> dict:
    return jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
