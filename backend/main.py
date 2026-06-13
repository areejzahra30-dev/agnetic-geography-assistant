import os
import asyncio
import json
import logging

# Load environment variables FIRST, before anything else
from dotenv import load_dotenv
# Load from .env.local first, then .env as fallback
load_dotenv(".env.local")
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set GROK_API_KEY from environment
GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    logger.warning("⚠️  GROK_API_KEY not set! Using mock responses. Set it in .env.local or .env file.")
else:
    logger.info("✅ GROK_API_KEY loaded successfully from environment")
    os.environ["GROK_API_KEY"] = GROK_API_KEY

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Agentic Geography Assistant",
    description="Backend API for geography queries with LLM agent",
    version="0.1.0",
)

# CORS configuration - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers from app
from app.api import chat, auth

# Include routers
app.include_router(chat.router)
app.include_router(auth.router)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "Agentic Geography Assistant"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic Geography Assistant Backend",
        "version": "0.1.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "uvicorn main:app --reload --host 0.0.0.0 --port 8000",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )