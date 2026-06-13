import asyncio
import json
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uuid

from app.models import create_in_memory_session, get_in_memory_session, add_message_to_session
from app.agent import get_agent

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatStartRequest(BaseModel):
    query: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str


@router.post("/start", response_model=dict)
async def start_chat(req: ChatStartRequest):
    """Start a new chat session"""
    # In production, extract user_id from session/token
    user_id = "demo-user-id"
    
    session = create_in_memory_session(user_id, title=req.query[:50])
    
    # Add user message
    add_message_to_session(session["id"], "user", req.query)
    
    return {
        "sessionId": session["id"],
        "id": session["id"],
    }


@router.get("/stream")
async def stream_chat(sessionId: str = Query(...)):
    """SSE endpoint for streaming assistant responses via grok-3-fast agent"""
    session = get_in_memory_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    async def generate():
        """Generator for SSE responses using the real agent"""
        try:
            # Extract the user's query from the first message
            user_query = session['messages'][0]['content'] if session['messages'] else "Unknown place"
            
            # Get the agent and stream place info
            agent = get_agent()
            full_response = {"description": "", "images": []}
            
            async for chunk in agent.stream_place_info(user_query):
                data = chunk
                yield f"data: {json.dumps(data)}\n\n"
                full_response[chunk.get("type", "message")] = chunk
            
            # Add full message to session
            add_message_to_session(sessionId, "assistant", full_response.get("description", ""))
            
            # Final done marker
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/{sessionId}/messages", response_model=list[MessageResponse])
async def get_session_messages(sessionId: str):
    """Fetch all messages in a session"""
    session = get_in_memory_session(sessionId)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return [
        MessageResponse(
            id=f"{sessionId}-msg-{i}",
            role=msg["role"],
            content=msg["content"],
        )
        for i, msg in enumerate(session["messages"])
    ]


@router.get("/sessions", response_model=list[dict])
async def list_sessions():
    """List all sessions for current user (simplified)"""
    # In production, filter by user_id from session/token
    from app.models import _in_memory_sessions
    return [
        {
            "id": sid,
            "title": sess["title"],
            "created_at": sess["created_at"].isoformat(),
        }
        for sid, sess in list(_in_memory_sessions.items())[:10]
    ]


@router.delete("/{sessionId}")
async def delete_session(sessionId: str):
    """Delete a chat session (GDPR/CCPA)"""
    from app.models import _in_memory_sessions
    
    if sessionId not in _in_memory_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del _in_memory_sessions[sessionId]
    return {"message": "Session deleted"}


@router.get("/export/user/{userId}")
async def export_user_data(userId: str):
    """Export user data (GDPR/CCPA)"""
    # Placeholder: fetch user and all their sessions/messages from DB
    return {
        "user_id": userId,
        "email": "user@example.com",
        "display_name": "User",
        "sessions": [],
        "exported_at": "2026-06-08T00:00:00Z",
    }
