from fastapi import APIRouter

routes = APIRouter(prefix="/v1/media", tags=["media"])

# TODO Return All Medias
@routes.get("/")
async def get_medias() -> dict:
    return {"media_status": "online"}

# TODO Return Media By ID
@routes.get("/{media_id}")
async def get_media_by_id(media_id: str) -> dict:
    return {"media": media_id}
