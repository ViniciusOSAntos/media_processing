from uuid import uuid4
from typing import List

from fastapi import UploadFile
from loguru import logger
from app.core.google import Google
from app.core.config import Settings

google = Google()
settings = Settings()

async def upload_media_service(
    files: List[UploadFile]
) -> dict:

    storage_client = google.get_storage_client()
    bucket_name = f"bkt-media-processing-{settings.environment}"

    logger.debug(f"List Buckets:::{storage_client.list_buckets()}")

    bucket = storage_client.bucket(bucket_name)

    if (
        not bucket.exists(client=storage_client)
        and settings.environment == "local"
    ):
        storage_client.create_bucket(bucket_name)

    for file in files:
        file_name = f"media-processing/{file.filename}"
        file_content = await file.read()
        blob = bucket.blob(file_name)
        blob.metadata = {
            "id": str(uuid4())
        }
        blob.upload_from_string(
            file_content, content_type=file.content_type
        )
