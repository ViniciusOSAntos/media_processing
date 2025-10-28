from fastapi import FastAPI

from app.api.healthcheck import setup_healthcheck

app = FastAPI(
    title="Media Processing API",
    version="v1",
    description=" ### API V1",
    debug=False,
)

setup_healthcheck(app)
