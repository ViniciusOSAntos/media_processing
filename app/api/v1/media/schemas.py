from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class MediaSchema(BaseModel):
    name: str = Field(
        ...,
        json_schema_extra={
            "description": "Blob file name",
            "exemple": "teste.mp4",
        }
    )
    created_at: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Blob creation time",
            "example": "2025-10-06T12:04:51.542978Z",
        }
    )
    updated_at: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Blob update time",
            "example": "2025-10-06T12:04:51.542978Z",
        }
    )

class MediaReturnSchema(MediaSchema):
    download_url: Optional[str] = Field(
        None,
        json_schema_extra={
            "description": "URL for media download",
            "example": "",
        }
    )
