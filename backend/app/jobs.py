"""
Background jobs for retention policies and cleanup.
Placeholder for APScheduler / Celery integration.
"""

from datetime import datetime, timedelta
from app.config import SESSION_RETENTION_DAYS
from app.models import cleanup_old_sessions


async def cleanup_expired_sessions():
    """
    Background job to delete chat sessions older than SESSION_RETENTION_DAYS.
    Run this periodically (e.g., daily via APScheduler).
    """
    deleted_count = cleanup_old_sessions(SESSION_RETENTION_DAYS)
    print(f"[Retention Job] Deleted {deleted_count} sessions older than {SESSION_RETENTION_DAYS} days")
    return deleted_count


async def cleanup_old_images():
    """
    Background job to delete cached images older than IMAGE_CACHE_TTL_DAYS.
    Requires S3/CDN implementation.
    """
    from app.image_cache import get_image_cache
    cache = get_image_cache()
    await cache.cleanup_old_cached_images()


# TODO: Wire these jobs with APScheduler on app startup
# Example:
#   from apscheduler.schedulers.asyncio import AsyncIOScheduler
#   scheduler = AsyncIOScheduler()
#   scheduler.add_job(cleanup_expired_sessions, 'cron', hour=0)  # Run daily at midnight
#   scheduler.start()
