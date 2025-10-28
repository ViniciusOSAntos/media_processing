from fastapi import FastAPI

from app.api.v1.media.routes import routes as media
from app.api.healthcheck import setup_healthcheck
app = FastAPI(
    title="Media Processing API",
    version="v1",
    description=" ### API V1",
    debug=False,
)

app.include_router(media)
setup_healthcheck(app)
