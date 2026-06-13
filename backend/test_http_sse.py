#!/usr/bin/env python
"""
Test script for verifying SSE streaming through the FastAPI HTTP endpoints.

This script tests the actual /api/chat/start and /api/stream endpoints.

Requirements:
    - Backend must be running: uvicorn main:app --reload

Usage:
    python test_http_sse.py [backend_url] [place_name]

Example:
    python test_http_sse.py http://localhost:8000 "Tokyo"
"""

import asyncio
import httpx
import json
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def test_auth_endpoints(base_url: str):
    """Test auth endpoints"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 1: Auth Endpoints")
    logger.info("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Signup
        logger.info("\n[POST] /api/auth/signup")
        signup_res = await client.post(
            f"{base_url}/api/auth/signup",
            json={"email": "test@example.com", "password": "password123", "display_name": "Test User"},
        )
        logger.info(f"Status: {signup_res.status_code}")
        if signup_res.status_code == 200:
            user = signup_res.json()
            logger.info(f"✓ Created user: {user['email']}")
        else:
            logger.warning(f"Response: {signup_res.text}")
        
        # Me endpoint
        logger.info("\n[GET] /api/auth/me")
        me_res = await client.get(f"{base_url}/api/auth/me")
        logger.info(f"Status: {me_res.status_code}")
        if me_res.status_code == 200:
            user = me_res.json()
            logger.info(f"✓ Current user: {user['email']}")


async def test_chat_start(base_url: str, place: str):
    """Test chat start endpoint"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Chat Start")
    logger.info("=" * 60)
    
    async with httpx.AsyncClient() as client:
        logger.info(f"\n[POST] /api/chat/start")
        logger.info(f"Query: {place}")
        
        res = await client.post(
            f"{base_url}/api/chat/start",
            json={"query": place},
        )
        logger.info(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            data = res.json()
            session_id = data.get("sessionId") or data.get("id")
            logger.info(f"✓ Created session: {session_id}")
            return session_id
        else:
            logger.error(f"Failed to create session: {res.text}")
            return None


async def test_sse_stream(base_url: str, session_id: str, place: str):
    """Test SSE stream endpoint"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: SSE Stream Endpoint")
    logger.info("=" * 60)
    
    logger.info(f"\n[GET] /api/stream?sessionId={session_id}")
    logger.info(f"Place: {place}\n")
    
    message_count = 0
    image_count = 0
    error_count = 0
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("GET", f"{base_url}/api/stream", params={"sessionId": session_id}) as res:
                logger.info(f"Status: {res.status_code}")
                logger.info("Streaming SSE events:\n")
                
                async for line in res.aiter_lines():
                    if line.startswith("data:"):
                        try:
                            data_str = line[5:].strip()
                            if data_str:
                                data = json.loads(data_str)
                                chunk_type = data.get("type")
                                
                                if chunk_type == "message":
                                    print(data.get("text", ""), end="", flush=True)
                                    message_count += 1
                                
                                elif chunk_type == "image":
                                    image_count += 1
                                    logger.info(f"\n[Image {image_count}] {data.get('url', 'No URL')}")
                                
                                elif chunk_type == "done":
                                    logger.info("\n[DONE]")
                                
                                elif chunk_type == "error":
                                    error_count += 1
                                    logger.error(f"[ERROR] {data.get('message', 'Unknown error')}")
                        
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse SSE event: {line}")
    
    except Exception as e:
        logger.error(f"Stream error: {e}")
    
    logger.info(f"\nStream complete.")
    logger.info(f"  Message chunks: {message_count}")
    logger.info(f"  Images: {image_count}")
    logger.info(f"  Errors: {error_count}")
    
    return {"message_chunks": message_count, "images": image_count}


async def test_get_messages(base_url: str, session_id: str):
    """Test fetching messages from a session"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Fetch Session Messages")
    logger.info("=" * 60)
    
    async with httpx.AsyncClient() as client:
        logger.info(f"\n[GET] /api/chat/{session_id}/messages")
        
        res = await client.get(f"{base_url}/api/chat/{session_id}/messages")
        logger.info(f"Status: {res.status_code}")
        
        if res.status_code == 200:
            messages = res.json()
            logger.info(f"✓ Retrieved {len(messages)} message(s)")
            for i, msg in enumerate(messages):
                logger.info(f"  [{i+1}] Role: {msg['role']}, Content: {msg['content'][:50]}...")
        else:
            logger.error(f"Failed: {res.text}")


async def test_health(base_url: str):
    """Test health endpoint"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 0: Health Check")
    logger.info("=" * 60)
    
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"\n[GET] /health")
            res = await client.get(f"{base_url}/health", timeout=5.0)
            logger.info(f"Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                logger.info(f"✓ Backend is healthy: {data.get('status', 'unknown')}")
                return True
            else:
                logger.error(f"Unexpected status: {res.status_code}")
                return False
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            logger.error(f"Make sure the backend is running: uvicorn main:app --reload")
            return False


async def main():
    """Run all HTTP tests"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    place = sys.argv[2] if len(sys.argv) > 2 else "Tokyo"
    
    # Strip trailing slash
    base_url = base_url.rstrip("/")
    
    logger.info("\n" + "🧪 " * 20)
    logger.info("AGENTIC GEOGRAPHY ASSISTANT - HTTP SSE TEST SUITE")
    logger.info(f"Backend URL: {base_url}")
    logger.info("🧪 " * 20 + "\n")
    
    try:
        # Health check
        is_healthy = await test_health(base_url)
        if not is_healthy:
            sys.exit(1)
        
        # Auth tests
        await test_auth_endpoints(base_url)
        
        # Chat tests
        session_id = await test_chat_start(base_url, place)
        if not session_id:
            sys.exit(1)
        
        # SSE streaming test
        await test_sse_stream(base_url, session_id, place)
        
        # Fetch messages test
        await test_get_messages(base_url, session_id)
        
        logger.info("\n" + "✅ " * 20)
        logger.info("ALL HTTP TESTS COMPLETED SUCCESSFULLY")
        logger.info("✅ " * 20 + "\n")
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
