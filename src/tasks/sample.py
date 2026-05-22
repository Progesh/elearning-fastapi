import time

from src.workers.celery_worker import celery_worker


@celery_worker.task(bind=True, max_retries=3, default_retry_delay=5)
def sample_task(self) -> str:
    try:
        time.sleep(10)
        return "Task completed successfully"
    except Exception as exc:
        raise self.retry(exc=exc)
