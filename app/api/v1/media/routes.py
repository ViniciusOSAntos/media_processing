from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status, Request
from sqlalchemy.orm import Session
from typing import Dict

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
)

routes = APIRouter(prefix="/v1/media", tags=["media"])

@routes.get(
    "/{media_name}",
    status_code=status.HTTP_200_OK,
    response_model=MediaReturnSchema
)
async def get_media_by_name(media_name: str) -> Dict[str, str]:
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
) -> List[Dict[str, str]]:

    return await upload_media_service(files, db)

@routes.delete(
    "/{media_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_media_by_name(media_name: str) -> None:
    await delete_media_by_name_service(media_name)
