from fastapi import APIRouter

routes = APIRouter(prefix="/v1/media", tags=["media"])

@routes.get("/")
async def get_medias() -> None:
    return {"media_status": "online"}
