from typing import Optional
from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


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

# name,codec, frame_rate, created_at, updated_at
class MediaMetadataSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        json_schema_extra={
            "description": "File name",
            "example": "teste.mp4"
        }
    )
    codec: str = Field(
        ...,
        json_schema_extra={
            "description": "Algoritmo de Encoder de vídeo",
            "example": "h.264"
        }
    )
    frame_rate: int = Field(
        ...,
        json_schema_extra={
            "description": "Número de quadros por segundo",
            "example": "60"
        }
    )
    # created_at: datetime = Field(
    #     ...,
    #     json_schema_extra={
    #         "description": "File creation time",
    #         "example": "2025-10-06T12:04:51.542978Z",
    #     }
    # )
    # updated_at: datetime = Field(
    #     ...,
    #     json_schema_extra={
    #         "description": "File creation time",
    #         "example": "2025-10-06T12:04:51.542978Z",
    #     }
    # )
