import os
import time
import logging
import datetime
from celery import Celery

from helper import stego_encode

celery = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

logger = logging.getLogger(__name__)


@celery.task(bind=True)
def encode_image_task(self, input_path, message, output_path):
    worker_name = getattr(self.request, "hostname", "unknown-worker")
    task_id = getattr(self.request, "id", None)
    start_ts = datetime.datetime.utcnow()

    # Log Information
    logger.info(
        "[%s] Worker %s START task=%s file=%s",
        start_ts.isoformat(),
        worker_name,
        task_id,
        os.path.basename(input_path),
    )

    try:
        time.sleep(3)

        stego_encode(input_path, message, output_path)

    except Exception as exc:
        logger.exception(
            "[%s] Worker %s FAILED task=%s file=%s error=%s",
            datetime.datetime.utcnow().isoformat(),
            worker_name,
            task_id,
            os.path.basename(input_path),
            exc,
        )
        raise

    end_ts = datetime.datetime.utcnow()
    elapsed = (end_ts - start_ts).total_seconds()
    logger.info(
        "[%s] Worker %s FINISH task=%s output=%s elapsed=%.3fs",
        end_ts.isoformat(),
        worker_name,
        task_id,
        os.path.basename(output_path),
        elapsed,
    )

    return output_path
