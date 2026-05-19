from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import Settings, get_settings
from src.core.security import decode_access_token

http_bearer = HTTPBearer()

SettingsDep = Annotated[Settings, Depends(get_settings)]


def require_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(http_bearer)],
    settings: SettingsDep,
) -> str:
    try:
        payload = decode_access_token(credentials.credentials, settings)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
