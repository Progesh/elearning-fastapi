from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.v1.api import api_router
from src.core.exceptions import AppException

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(api_router, prefix="/api/v1")
