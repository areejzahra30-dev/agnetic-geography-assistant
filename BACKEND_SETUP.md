CORS & hosting
- Since frontend will be hosted on Vercel/Netlify and backend on Render/Railway, configure CORS to allow:
	- `http://localhost:3000`
	- `https://app.domain.com`
	- `https://api.domain.com`

Example FastAPI CORS middleware:
```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
		"http://localhost:3000",
		"https://app.domain.com",
		"https://api.domain.com",
]

app.add_middleware(
		CORSMiddleware,
		allow_origins=origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
)
```

Retention (30 days)
- Implement a periodic background job (e.g., `APScheduler`, Celery beat, or a simple cron) that deletes chat/session records older than 30 days. Make retention configurable via env var `SESSION_RETENTION_DAYS`.

Image caching
- Store images returned by MCP servers in object storage (S3 / DigitalOcean Spaces) or a CDN. Save references in the `Place` model and serve proxied URLs to the frontend to avoid exposing third-party keys.

Backend Setup — FastAPI + OpenAI Agents SDK + litellm quickstart

Prerequisites
- Python 3.11+
- git
- access to Neon Postgres instance
- LLM API key (OpenAI/Grok provider) and MCP credentials

Create & activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install --upgrade pip
```

Install core dependencies (example)
```bash
pip install fastapi uvicorn[standard] sqlalchemy alembic asyncpg
pip install openai-agents-sdk litellm pexels-mcp-server
# plus any MCP or scraping libs you need
```

Project skeleton
- `app/main.py` — FastAPI app and routes
- `app/api/auth.py` — auth endpoints (signup/login/logout/me)
- `app/api/places.py` — place / chat endpoints
- `app/db/` — models, migrations (alembic)
- `app/agents/` — agent orchestration and tool connectors

Environment variables (example)
```
DATABASE_URL=postgresql://user:pass@db.host:5432/dbname
SECRET_KEY=your-secret
GROK_API_KEY=your-grok-key
MCP_APIFY_HEADER=Authorization: <token>
PEXELS_API_KEY=your-pexels-key
ALLOWED_ORIGINS=http://localhost:3000
```

Running locally
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Agent wiring notes
- Configure litellm to use the grok model you have access to; test a small prompt locally
- Implement tool wrappers for MCP servers so the agent can call them safely (do not expose keys to frontend)

DB migrations
- Initialize Alembic and create migrations for User, Session, Message, Place models

Streaming
- If you need streaming responses to frontend, implement SSE endpoints in FastAPI or use WebSocket; make sure frontend supports chosen mechanism

Production
- Use HTTPS and a process manager (gunicorn/uvicorn workers) behind a reverse proxy
- Use secrets manager for keys rather than env files in production
