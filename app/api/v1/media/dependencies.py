import os
import ffmpeg
import json
import shutil

from fastapi import UploadFile
from loguru import logger

UPLOAD_DIR = "tmp"

async def iterate_blobs(blobs, prefix_params, media_name) -> dict:
    for blob in blobs:
        logger.debug(blob.name)
        if blob.name == f"{prefix_params.get('prefix')}/{media_name}":
            logger.success(f"Media Found {blob.name}")
            metadata = blob.metadata or {}

            return blob
async def save_file_tmp(file: UploadFile):
    file_location = f"./{UPLOAD_DIR}/{file.filename}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(file_location, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        buffer.flush()
        os.fsync(buffer.fileno())
        logger.debug(f"File: {file.filename} saved in tmp")

async def delete_file_tmp(file_name: str):
    file_location = f"./{UPLOAD_DIR}/{file_name}"
    if os.path.exists(file_location):
        os.remove(f"./{UPLOAD_DIR}/{file_name}")
        logger.debug("File Deleted")
    else:
        logger.debug(f"Delete file failed, file {file_location} does NOT exist")

async def get_video_metadata(file_name: str):
    file_location = f"./{UPLOAD_DIR}/{file_name}"
    logger.debug(f"File Location: {file_location}")
    try:
        video_metadata = ffmpeg.probe(file_location)
    except Exception as e:
        logger.error(f"Erro no probe: {e.stderr.decode('utf-8', errors='ignore')}")
    logger.debug(
        "Video Metadata:\n{}",
        json.dumps(video_metadata, indent=4, ensure_ascii=False)
    )

    return video_metadata
