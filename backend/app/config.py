import os
from dotenv import load_dotenv

load_dotenv()

# Database (using psycopg2 driver for Windows compatibility)
# Format: postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/agentic_geo")

# Secret key for tokens (session/JWT if using)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# LLM
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
GROK_MODEL = "xai/grok-3-fast"

# MCP / external
MCP_APIFY_HEADER = os.getenv("MCP_APIFY_HEADER", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://app.domain.com,https://api.domain.com").split(",")

# Retention (days)
SESSION_RETENTION_DAYS = int(os.getenv("SESSION_RETENTION_DAYS", "30"))

# Image cache config (S3 / CDN placeholder)
IMAGE_CACHE_BUCKET = os.getenv("IMAGE_CACHE_BUCKET", "agentic-geo-images")
IMAGE_CACHE_TTL_DAYS = int(os.getenv("IMAGE_CACHE_TTL_DAYS", "90"))
