import os
from celery import Celery
from helper import stego_encode

# Initialize Celery app
celery = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

@celery.task
def encode_image_task(input_path, message, output_path):
    """Encodes a message into an image and saves the output."""
    stego_encode(input_path, message, output_path)
    return output_path
