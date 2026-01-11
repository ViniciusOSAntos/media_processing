from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status, Request
from sqlalchemy.orm import Session

from app.api.v1.media.services import (
    upload_media_service,
    get_media_by_name_service,
    delete_media_by_name_service,
    create_video_metadata,
    save_file_tmp,
    delete_file_tmp,
    get_video_metadata
)

from app.api.v1.media.db import (
    get_db
)

from app.api.v1.media.schemas import (
    MediaReturnSchema,
    MediaMetadataSchema
)

routes = APIRouter(prefix="/v1/media", tags=["media"])

@routes.get(
    "/{media_name}",
    status_code=status.HTTP_200_OK,
    response_model=MediaReturnSchema
)
async def get_media_by_name(media_name: str) -> dict:
    return await get_media_by_name_service(media_name)


@routes.put(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=List[MediaReturnSchema]
)
async def create_media(
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
) -> List[dict]:
    mock_metadata = {
        "name": "video_teste.mp4",
        "codec": "h.264",
        "frame_rate": 30,
    }
    video_metadata = MediaMetadataSchema(**mock_metadata)
    await save_file_tmp(files[0])
    await get_video_metadata(files[0].filename)
    await create_video_metadata(db, video_metadata)
    await delete_file_tmp(files[0].filename)

    return await upload_media_service(files)

@routes.delete(
    "/{media_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_media_by_name(media_name: str):
    await delete_media_by_name_service(media_name)
