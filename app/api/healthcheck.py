from fastapi import FastAPI, status
from pydantic import BaseModel

class HealthCheck(BaseModel):

    status: str = "ONLINE"

def setup_healthcheck(app: FastAPI) -> None:
    @app.get(
        "/healthcheck",
        tags=["healthcheck"],
        summary="Perform a Health Check",
        response_description="Return HTTP Status Code 200 (OK)",
        status_code=status.HTTP_200_OK,
        response_model=HealthCheck,
    )
    def healthcheck() -> HealthCheck:
        return HealthCheck(status="ONLINE")
