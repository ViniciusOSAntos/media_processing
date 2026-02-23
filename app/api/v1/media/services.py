from uuid import uuid4
from typing import List, Dict
from datetime import timedelta

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from loguru import logger
from app.core.google import Google
from app.core.config import Settings
from app.api.v1.media.dependencies import (
    iterate_blobs,
    save_file_tmp,
    delete_file_tmp,
    get_video_metadata
)
from app.api.v1.media import models, schemas


google = Google()
settings = Settings()

async def upload_media_service(
    files: List[UploadFile],
    db: Session
) -> List[dict]:
    # queria ajuda para estruturar os tratamentos de excessão
    # DB Conn
    return_metadata = []
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
        metadata = {}
        file_name = f"media-processing/{file.filename}"
        file_content = await file.read()
        blob = bucket.blob(file_name)
        id_blob = str(uuid4())
        blob.metadata = {
            "id": id_blob
        }
        blob.upload_from_string(
            file_content, content_type=file.content_type
        )
        blob.make_public() # A princípio todas a mídias serão públicas
        metadata["name"] = file.filename
        metadata["id"] = id_blob
        metadata["created_at"] = blob.time_created
        metadata["updated_at"] = blob.updated
        metadata["download_url"] = blob.public_url

        return_metadata.append(metadata)

        await file.seek(0)
        temp_file = await save_file_tmp(file)
        video_metadata = await get_video_metadata(temp_file)
        schemas.MediaMetadataSchema.model_validate(video_metadata)
        logger.debug(video_metadata)

        await create_video_metadata(db, video_metadata) # Insere no banco
        await delete_file_tmp(temp_file)


    storage_client.close()

    return return_metadata

async def get_media_by_name_service(
    media_name: str
) -> Dict[str, str]:
    # queria ajuda para estruturar os tratamentos de excessão
    storage_client = google.get_storage_client()
    bucket_name = f"bkt-media-processing-{settings.environment}"
    bucket = storage_client.bucket(bucket_name)
    prefix_params = {"prefix": "media-processing"}

    blobs = bucket.list_blobs()
    logger.debug(blobs)

    blob_found = await iterate_blobs(
        blobs=blobs,
        prefix_params=prefix_params,
        media_name=media_name
    )

    if blob_found:
        metadata = blob_found.metadata or {}
        return {
            "name": blob_found.name,
            "id": metadata.get("id"),
            "created_at": blob_found.time_created,
            "updated_at": blob_found.updated,
            "download_url": blob_found.public_url,
        }

    raise HTTPException(
        status_code=404,
        detail="Media not found."
    )

async def delete_media_by_name_service(
    media_name: str
):
    storage_client = google.get_storage_client()
    bucket_name = f"bkt-media-processing-{settings.environment}"
    bucket = storage_client.bucket(bucket_name)
    prefix_params = {"prefix": "media-processing"}

    blobs = bucket.list_blobs()
    logger.debug(blobs)

    blob_found = await iterate_blobs(
        blobs=blobs,
        prefix_params=prefix_params,
        media_name=media_name
    )

    if blob_found:
        blob_found.delete()

async def create_video_metadata(db: Session, video_metadata: Dict[str, str]):
    new_video_metadata = models.VideoMetadata(
        name=video_metadata.get("name"),
        codec=video_metadata.get("codec"),
        frame_rate=video_metadata.get("frame_rate")
    )
    db.add(new_video_metadata)
    db.commit()
    db.refresh(new_video_metadata)

    return new_video_metadata
