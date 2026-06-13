"""
Image caching and storage helpers.
Placeholder for S3/CDN integration.
"""

from datetime import datetime
from app.config import IMAGE_CACHE_BUCKET, IMAGE_CACHE_TTL_DAYS


class ImageCache:
    """
    Manages caching of images from MCP sources (Pexels, Apify).
    In production, uses S3 or CDN.
    """
    
    def __init__(self):
        # TODO: Initialize S3 / CDN client (boto3, etc.)
        self.bucket = IMAGE_CACHE_BUCKET
        self.ttl_days = IMAGE_CACHE_TTL_DAYS
    
    async def cache_image(self, source_url: str, place_name: str) -> str:
        """
        Download image from source and cache in S3/CDN.
        Returns the cached image URL.
        """
        # TODO: Implement download, upload to S3, and return CDN URL
        # Placeholder: return source URL as-is
        return source_url
    
    async def cache_images_for_place(self, place_name: str, image_urls: list[str]) -> list[str]:
        """Cache multiple images for a place"""
        cached_urls = []
        for url in image_urls:
            cached_url = await self.cache_image(url, place_name)
            cached_urls.append(cached_url)
        return cached_urls
    
    async def cleanup_old_cached_images(self):
        """Delete cached images older than TTL (run as background job)"""
        # TODO: Implement S3 listing and cleanup
        pass


_cache = None


def get_image_cache() -> ImageCache:
    global _cache
    if _cache is None:
        _cache = ImageCache()
    return _cache
