# Agentic Geography Assistant — Backend (FastAPI)

This folder contains the FastAPI backend for the agentic geography assistant. It provides:
- Auth endpoints (email + password, no email verification)
- Chat session management
- SSE streaming for progressive LLM responses
- In-memory session storage (with Neon Postgres placeholders)
- Image caching stubs (for S3/CDN)
- **LLM Agent** with grok-3-fast via litellm + tool integration (Apify, Pexels MCP)

## Quick Start

### Windows Users

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for step-by-step guide using `psycopg2-binary`.

### macOS / Linux Users

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment setup

```bash
cp .env.example .env.local
# Edit .env.local and set your keys:
# - GROK_API_KEY (Grok model access)
# - MCP_APIFY_HEADER (Apify auth)
# - PEXELS_API_KEY (Pexels images)
# - DATABASE_URL (Neon Postgres — optional for local dev)
```

### 3. Run dev server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`.

Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI).

## API Endpoints

### Auth (`/api/auth/`)
- **POST** `/signup` — Register with email + password
- **POST** `/login` — Login with email + password
- **POST** `/logout` — Logout and clear session
- **GET** `/me` — Get current user info

### Chat (`/api/chat/`)
- **POST** `/start` — Start a new chat session → `{sessionId}`
- **GET** `/stream?sessionId=...` — SSE stream for progressive assistant responses
- **GET** `/{sessionId}/messages` — Fetch all messages in session
- **GET** `/sessions` — List all sessions (demo)
- **DELETE** `/{sessionId}` — Delete a session (GDPR/CCPA)
- **GET** `/export/user/{userId}` — Export user data (GDPR/CCPA)

### Health
- **GET** `/health` — Health check
- **GET** `/` — Root / info

## Architecture

### Current state (local dev)
- In-memory session storage (not persistent, but ready for Neon Postgres)
- **✅ LLM Agent** with grok-3-fast via litellm + tool integration
- **✅ SSE Streaming** for progressive responses
- Placeholder image caching (returns URLs as-is)
- Placeholder MCP tool integration (structure in place)
- psycopg2-binary driver (Windows-compatible)

### Production roadmap
1. **Database**: Migrate from in-memory to Neon Postgres using SQLAlchemy + psycopg2
2. **Agent**: Integrate real MCP tool calls (Apify, Pexels) into agent
3. **Image cache**: Implement S3 upload and CDN serving
4. **Jobs**: Add APScheduler for session retention cleanup
5. **Auth**: Integrate BetterAuth or JWT token validation

### Files

- `main.py` — FastAPI app, CORS, routers
- `app/config.py` — Configuration from env (psycopg2 driver)
- `app/db.py` — Database connection helpers (SQLAlchemy + psycopg2)
- `app/models.py` — SQLAlchemy ORM models + in-memory store helpers
- `app/api/auth.py` — Auth endpoints (signup, login, logout, me)
- `app/api/chat.py` — Chat + SSE endpoints with real agent integration
- `app/agent.py` — **✅ LLM Agent** (grok-3-fast via litellm + tool definitions)
- `app/image_cache.py` — Image caching helper (S3/CDN placeholder)
- `app/jobs.py` — Background job stubs (retention cleanup)
- `test_agent.py` — Direct agent testing (no HTTP)
- `test_http_sse.py` — HTTP endpoint + SSE testing

## Testing the full flow (local)

1. Start backend: `uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to `http://localhost:3000`
4. Use the demo sign-in (or create an account)
5. Ask about a place (e.g., "Tokyo")
6. Watch SSE stream the response + images in real-time

## GDPR/CCPA compliance

- **Export**: `GET /api/export/user/{userId}` returns user data
- **Delete**: `DELETE /api/chat/{sessionId}` removes session; extend to user deletion
- **Retention**: Sessions auto-purge after `SESSION_RETENTION_DAYS` (default 30 days)
- **Audit**: Log deletion/export requests (TODO)

## Next steps

- Implement OpenAI Agents SDK + litellm for grok-3-fast integration
- Connect MCP Apify and Pexels servers
- Migrate sessions to Neon Postgres
- Add background job scheduler (APScheduler)
- Add comprehensive error handling and logging
- Add request rate-limiting (Redis)

## Notes

- For production, do NOT use in-memory storage; always persist to DB
- Secure all keys in a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Use environment-specific CORS origins (dev vs. prod)
- Consider adding request signing for sensitive endpoints
