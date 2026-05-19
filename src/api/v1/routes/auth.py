import hmac

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.core.dependencies import SettingsDep
from src.core.security import create_access_token

router = APIRouter()


class TokenRequest(BaseModel):
    client_id: str = Field(min_length=1)
    client_secret: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/token", response_model=TokenResponse)
def generate_token(body: TokenRequest, settings: SettingsDep) -> TokenResponse:
    id_match = hmac.compare_digest(body.client_id, settings.API_CLIENT_ID)
    secret_match = hmac.compare_digest(body.client_secret, settings.API_CLIENT_SECRET)

    if not id_match or not secret_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token, expires_in = create_access_token(settings)
    return TokenResponse(access_token=token, expires_in=expires_in)
