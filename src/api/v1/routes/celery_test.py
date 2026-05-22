from fastapi import APIRouter
from pydantic import BaseModel

from src.tasks.sample import sample_task

router = APIRouter()


class TaskResponse(BaseModel):
    task_id: str
    message: str


@router.post("/test", response_model=TaskResponse)
def trigger_test_task() -> TaskResponse:
    task = sample_task.delay()
    return TaskResponse(
        task_id=task.id,
        message="Task dispatched successfully. It will complete in ~10 seconds. Auto-retries up to 3 times on failure.",
    )
