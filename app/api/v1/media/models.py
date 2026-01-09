from sqlalchemy import Column, Integer, String, DateTime, func
from app.api.v1.media.db import Base
from loguru import logger

class VideoMetadata(Base):
    __tablename__ = "video_metadata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    codec = Column(String(50), nullable=False)
    # width = Column(Integer, nullable=False),
    # height = Column(Integer, nullable=False),
    frame_rate = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
