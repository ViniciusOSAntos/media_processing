from typing import List
from fastapi import APIRouter, UploadFile, File, status, Request

from app.api.v1.media.services import (
    upload_media_service,
    get_media_by_name_service,
    delete_media_by_name_service
)

from app.api.v1.media.schemas import (
    MediaReturnSchema
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
) -> List[dict]:
    return await upload_media_service(files)

@routes.delete(
    "/{media_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_media_by_name(media_name: str):
    await delete_media_by_name_service(media_name)
