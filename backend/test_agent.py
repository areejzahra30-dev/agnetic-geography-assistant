#!/usr/bin/env python
"""
Test script for verifying agent responses through SSE streaming.

Usage:
    python test_agent.py [place_name]

Example:
    python test_agent.py "Tokyo"
    python test_agent.py "Paris"
"""

import asyncio
import json
import sys
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Setup path
sys.path.insert(0, "/".join(__file__.split("/")[:-1]))

from app.models import create_in_memory_session, get_in_memory_session, add_message_to_session
from app.agent import get_agent


async def test_agent_direct():
    """Test the agent directly (no HTTP)"""
    logger.info("=" * 60)
    logger.info("TEST 1: Direct Agent Query")
    logger.info("=" * 60)
    
    agent = get_agent()
    place = "Tokyo"
    
    logger.info(f"\nQuerying place: {place}")
    response = await agent.query_place(place)
    
    logger.info(f"\nAgent Response:")
    logger.info(f"  Place: {response['place']}")
    logger.info(f"  Description: {response['description'][:100]}...")
    logger.info(f"  Images: {len(response['image_urls'])} image(s)")
    for i, img in enumerate(response['image_urls']):
        logger.info(f"    [{i+1}] {img}")
    
    return response


async def test_agent_streaming():
    """Test the agent with streaming output"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Streaming Agent Output (SSE simulation)")
    logger.info("=" * 60)
    
    agent = get_agent()
    place = "Paris"
    
    logger.info(f"\nStreaming place info: {place}")
    logger.info("Messages:")
    
    message_count = 0
    image_count = 0
    
    async for chunk in agent.stream_place_info(place):
        chunk_type = chunk.get("type")
        
        if chunk_type == "message":
            print(chunk.get("text", ""), end="", flush=True)
            message_count += 1
        
        elif chunk_type == "image":
            image_count += 1
            logger.info(f"\n[Image {image_count}] {chunk.get('url', 'No URL')}")
    
    logger.info(f"\n\nStream complete. Received {message_count} message chunks and {image_count} images.")
    return {"message_chunks": message_count, "images": image_count}


async def test_session_workflow():
    """Test the full session workflow"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Full Session Workflow")
    logger.info("=" * 60)
    
    user_id = "test-user-123"
    place_query = "Tokyo"
    
    # Create session
    session = create_in_memory_session(user_id, title=place_query)
    logger.info(f"\nCreated session: {session['id']}")
    logger.info(f"User ID: {user_id}")
    
    # Add user message
    msg = add_message_to_session(session["id"], "user", place_query)
    logger.info(f"Added user message: {place_query}")
    
    # Stream agent response
    logger.info("\nStreaming agent response...")
    agent = get_agent()
    
    full_response = ""
    image_urls = []
    
    async for chunk in agent.stream_place_info(place_query):
        if chunk.get("type") == "message":
            full_response += chunk.get("text", "")
        elif chunk.get("type") == "image":
            image_urls.append(chunk.get("url"))
    
    # Add assistant message to session
    add_message_to_session(session["id"], "assistant", full_response)
    logger.info(f"Added assistant response ({len(full_response)} chars)")
    
    # Fetch session to verify
    fetched_session = get_in_memory_session(session["id"])
    logger.info(f"\nSession messages: {len(fetched_session['messages'])}")
    for i, msg in enumerate(fetched_session["messages"]):
        logger.info(f"  [{i+1}] Role: {msg['role']}, Content: {msg['content'][:50]}...")
    
    return fetched_session


async def test_sse_endpoint_simulation():
    """Simulate what the SSE endpoint does"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: SSE Endpoint Simulation")
    logger.info("=" * 60)
    
    # Simulate endpoint logic
    place = "Barcelona"
    session = create_in_memory_session("test-user", title=place)
    add_message_to_session(session["id"], "user", place)
    
    logger.info(f"Simulating /api/stream endpoint for: {place}")
    logger.info("SSE events:")
    
    agent = get_agent()
    events = []
    
    async for chunk in agent.stream_place_info(place):
        # Format as SSE
        sse_event = f"data: {json.dumps(chunk)}\n\n"
        events.append(sse_event)
        
        chunk_type = chunk.get("type")
        if chunk_type == "message":
            print(f"  [MESSAGE] {chunk.get('text', '')}", end="")
        elif chunk_type == "image":
            logger.info(f"\n  [IMAGE] {chunk.get('url', '')}")
    
    # Add done marker
    done_event = f"data: {json.dumps({'type': 'done'})}\n\n"
    events.append(done_event)
    logger.info("\n  [DONE]")
    
    logger.info(f"\nTotal SSE events: {len(events)}")
    return events


async def main():
    """Run all tests"""
    place = sys.argv[1] if len(sys.argv) > 1 else None
    
    logger.info("\n" + "🧪 " * 20)
    logger.info("AGENTIC GEOGRAPHY ASSISTANT - AGENT TEST SUITE")
    logger.info("🧪 " * 20 + "\n")
    
    try:
        # Test 1: Direct agent query
        await test_agent_direct()
        
        # Test 2: Streaming
        await test_agent_streaming()
        
        # Test 3: Session workflow
        await test_session_workflow()
        
        # Test 4: SSE simulation
        await test_sse_endpoint_simulation()
        
        logger.info("\n" + "✅ " * 20)
        logger.info("ALL TESTS COMPLETED SUCCESSFULLY")
        logger.info("✅ " * 20 + "\n")
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
