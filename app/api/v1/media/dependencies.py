import os
import ffmpeg
import json
import shutil
import pathlib

from fastapi import UploadFile
from loguru import logger
from typing import List, Dict
from google.cloud.storage import Blob
from tempfile import NamedTemporaryFile, gettempdir


UPLOAD_DIR = "tmp"

async def iterate_blobs(blobs: List[Blob] , prefix_params: Dict[str, str], media_name: str) -> Blob | None:
    for blob in blobs:
        logger.debug(blob.name)
        if blob.name == f"{prefix_params.get('prefix')}/{media_name}":
            logger.success(f"Media Found {blob.name}")
            metadata = blob.metadata or {}

            return blob
    return None

async def save_file_tmp(file: UploadFile) -> str:
    if file.filename is None:
        raise ValueError("File Name is Required")

    suffix = pathlib.Path(file.filename).suffix
    with NamedTemporaryFile(
        mode='w+b',
        delete=False,
        suffix=suffix
    ) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        logger.debug(gettempdir())
        return temp_file.name

async def delete_file_tmp(file_name: str) -> None:
    if os.path.exists(file_name):
        os.remove(file_name)
        logger.debug("Temp File Deleted")
    else:
        logger.error(f"Delete file failed, file {file_name} does NOT exist")

async def get_video_metadata(file_name: str) -> Dict[str, str]:
    file_location = file_name
    logger.debug(f"File Location: {file_location}")
    return_metadata = {}
    try:
        video_metadata = ffmpeg.probe(file_location)

        return_metadata["name"] = (
            video_metadata
            .get("format", {})
            .get("filename", "")
            .split("/")[-1]
        )

        return_metadata["codec"] = (
            video_metadata
            .get("streams", {})[0]
            .get("codec_name", "")
        )

    except Exception as e:
        if e.stderr.decode('utf-8', errors='ignore').startswith("ffprobe"):
            logger.error(f"Erro no probe: {e.stderr.decode('utf-8', errors='ignore')}")
            video_metadata = None
        else:
            logger.error(f"Erro no probe: {e}")

    logger.debug(
        "Video Metadata:\n{}",
        json.dumps(video_metadata, indent=4, ensure_ascii=False)
    )

    return return_metadata
