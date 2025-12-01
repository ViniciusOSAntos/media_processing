from loguru import logger
async def iterate_blobs(blobs, prefix_params, media_name) -> dict:
    for blob in blobs:
        logger.debug(blob.name)
        if blob.name == f"{prefix_params.get('prefix')}/{media_name}":
            logger.success(f"Media Found {blob.name}")
            metadata = blob.metadata or {}
            
            return blob
