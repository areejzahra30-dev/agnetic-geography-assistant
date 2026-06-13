# Agent Testing Guide

This guide explains how to test the LLM agent wiring and SSE streaming in the Agentic Geography Assistant backend.

## Overview

The backend has been scaffolded with:
- **LLM Agent** (`app/agent.py`) — Uses `litellm` to call `grok-3-fast` model via OpenAI-compatible API
- **Tool Definitions** — Place info retrieval (Apify placeholder) and image search (Pexels placeholder)
- **SSE Endpoint** (`/api/stream`) — Streams progressive responses as JSON events
- **Test Scripts** — Direct agent testing and HTTP endpoint testing

## Test Scripts

### 1. Direct Agent Test (No HTTP)

Test the agent logic directly in Python without starting the HTTP server.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run all agent tests
python test_agent.py

# Or test a specific place
python test_agent.py "Paris"
```

**What it tests:**
- Direct agent query (mock response if `GROK_API_KEY` is not set)
- Streaming output from the agent
- Full session workflow (create session, stream response, store message)
- SSE event formatting simulation

**Expected output:**
```
🧪 🧪 🧪 ...
AGENTIC GEOGRAPHY ASSISTANT - AGENT TEST SUITE
✅ All tests completed successfully
```

### 2. HTTP SSE Endpoint Test

Test the actual FastAPI endpoints with HTTP requests. **Requires backend to be running.**

Terminal 1 (Backend):
```bash
cd backend
uvicorn main:app --reload
```

Terminal 2 (Tests):
```bash
cd backend

# Run all HTTP tests against localhost:8000
python test_http_sse.py

# Or specify backend URL and place
python test_http_sse.py http://localhost:8000 "Tokyo"

# Production example
python test_http_sse.py https://api.domain.com "Paris"
```

**What it tests:**
- Health check (`/health`)
- Auth endpoints (`/api/auth/signup`, `/api/auth/login`, `/api/auth/me`)
- Chat start (`POST /api/chat/start`)
- **SSE streaming** (`GET /api/stream?sessionId=...`)
- Message retrieval (`GET /api/chat/{sessionId}/messages`)

**Expected output:**
```
Status: 200
✓ Backend is healthy: ok

[POST] /api/auth/signup
Status: 200
✓ Created user: test@example.com

[GET] /api/stream?sessionId=...
Status: 200
Streaming SSE events:

[MESSAGE] Here's information about Tokyo...
[Image 1] https://images.pexels.com/...
[DONE]

Stream complete.
  Message chunks: 150
  Images: 3
```

## Configuration

### Backend Environment

Create `backend/.env.local` with:

```env
# Required for live grok-3-fast responses
GROK_API_KEY=your-grok-api-key-here

# Optional: MCP tool credentials
MCP_APIFY_HEADER=Authorization: your-apify-token
PEXELS_API_KEY=your-pexels-key

# CORS origins (adjust for your deployment)
ALLOWED_ORIGINS=http://localhost:3000,https://app.domain.com,https://api.domain.com

# Retention & caching config
SESSION_RETENTION_DAYS=30
IMAGE_CACHE_TTL_DAYS=90
```

### Notes

- **Without GROK_API_KEY**: Agent returns mock responses (good for testing UI)
- **With GROK_API_KEY**: Agent calls the real grok-3-fast model via litellm
- MCP tool functions are currently placeholders; extend `_execute_tool()` in `app/agent.py` to integrate real Apify/Pexels MCP servers

## SSE Event Format

The `/api/stream` endpoint returns Server-Sent Events in this format:

### Message Chunk
```json
{
  "type": "message",
  "text": "word "
}
```

### Image
```json
{
  "type": "image",
  "url": "https://example.com/image.jpg"
}
```

### Done Marker
```json
{
  "type": "done"
}
```

### Error (if any)
```json
{
  "type": "error",
  "message": "Error description"
}
```

## Frontend Integration

The frontend (Next.js example) listens to this stream in `pages/index.tsx`:

```typescript
async for (let chunk of agent.stream_place_info(place)):
  if (chunk.type === "message") print(chunk.text)
  if (chunk.type === "image") displayImage(chunk.url)
```

See `frontend/lib/betterAuth.ts` and `frontend/pages/index.tsx` for full implementation.

## Next Steps

### 1. Integrate Real MCP Tools

Currently, tool execution in `app/agent.py` returns mock data. To integrate real tools:

**Apify MCP** (place information scraping):
```python
# In _execute_tool("get_place_info", ...)
result = await call_apify_mcp_server(place_name)  # TODO: implement
```

**Pexels MCP** (image search):
```python
# In _execute_tool("search_place_images", ...)
images = await call_pexels_mcp_server(place_name, count)  # TODO: implement
```

### 2. Migrate to Neon Postgres

Currently using in-memory session storage. To use Neon:

1. Initialize Alembic: `alembic init migrations`
2. Create models: `alembic revision --autogenerate -m "Add initial schema"`
3. Apply migrations: `alembic upgrade head`
4. Update `app/models.py` to use async SQLAlchemy instead of in-memory dicts

### 3. Add Background Retention Job

Schedule the cleanup job to run periodically:

```python
# In main.py, on startup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(cleanup_expired_sessions, 'cron', hour=0)  # Daily at midnight
scheduler.start()
```

### 4. Production Deployment

- Deploy backend to Render/Railway with env vars set in secrets
- Deploy frontend to Vercel/Netlify with `NEXT_PUBLIC_API_BASE_URL` pointing to production backend
- Configure CORS to allow production domains
- Set up monitoring and error logging (Sentry, etc.)

## Troubleshooting

### Backend won't start
```
ModuleNotFoundError: No module named 'openai'
```
Solution: `pip install -r requirements.txt`

### SSE stream returns error
```json
{"type": "error", "message": "Session not found"}
```
Solution: Make sure `sessionId` from `/api/chat/start` is passed to `/api/stream`

### Agent returns mock responses
```
"Description: ... (mock response — set GROK_API_KEY for live responses)"
```
Solution: Set `GROK_API_KEY` in `.env.local` and restart backend

### Frontend doesn't connect to backend
```
CORS error: Access-Control-Allow-Origin
```
Solution: Update `ALLOWED_ORIGINS` in `backend/.env.local` to include frontend origin

## Quick Start (Full End-to-End)

Terminal 1 — Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local
# Edit .env.local and set GROK_API_KEY if you have it
uvicorn main:app --reload
```

Terminal 2 — Frontend:
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
npm run dev
```

Terminal 3 — Test SSE (optional):
```bash
cd backend
python test_http_sse.py http://localhost:8000 "Tokyo"
```

Then visit `http://localhost:3000` and try asking about a place!
