from typing import List
from fastapi import APIRouter, UploadFile, File, status, Request

from app.api.v1.media.services import (
    upload_media_service
)

routes = APIRouter(prefix="/v1/media", tags=["media"])

# TODO Return All Medias
@routes.get("/")
async def get_medias() -> dict:
    return {"media_status": "online"}

# TODO Return Media By ID
@routes.get("/{media_id}")
async def get_media_by_id(media_id: str) -> dict:
    return {"media": media_id}

@routes.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def create_media(
    request: Request,
    files: List[UploadFile] = File(...),
) -> List[dict]:
    await upload_media_service(files)
    return [{"Media": "Created"}]
