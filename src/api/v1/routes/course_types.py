from fastapi import APIRouter, Depends

from src.core.dependencies import require_auth
from src.core.database import DbSession

router = APIRouter(dependencies=[Depends(require_auth)])


@router.get("/")
def index(db: DbSession):
    return {"test": "test"}
