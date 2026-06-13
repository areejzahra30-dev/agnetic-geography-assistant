Back-end Requirements — Agentic Geography Assistant
Chosen configuration (from user)
- LLM model: `grok-3-fast` (user has API key)
- Images: stored/cached on backend (recommended: object storage like S3)
- Streaming: progressive assistant output required (SSE or WebSocket)
- Auth: email + password only, NO email verification
- Hosting: backend planned on Render or Railway; allow CORS for local and production domains
- Retention policy: default 30 days for chat/session data


Purpose: implement the agent and API surface using Python + FastAPI. The backend runs the OpenAI Agents SDK (agent orchestration), uses `litellm` to call the chosen LLM (grok-3-fast or grok-3-mini), calls MCP servers for scraping and image search, and persists users and chat sessions in Neon Postgres.

Core goals
- Secure API that serves the frontend: auth, place queries, chat sessions, image URLs
- LLM agent orchestration that can call external tools (MCP servers) and return structured responses
- Persist user accounts and chat/session history to Neon Postgres
- GDPR/CCPA compliance: endpoints for export, deletion, consent tracking

Tech stack & dependencies
- Python 3.11+ recommended
- Framework: FastAPI
- ASGI server: Uvicorn or Hypercorn
- ORM: SQLAlchemy 1.4+ (async) or SQLModel, with asyncpg driver
- Migrations: Alembic
- LLM & agent: OpenAI Agents SDK (Python) + litellm client configured to use Grok 3 models
- MCP connectors:
  - Apify MCP remote: via `npx mcp-remote` usage from config or backend HTTP calls to a proxy
  - Pexels MCP server: `pip install pexels-mcp-server` (user-provided)
- Authentication integration: BetterAuth (validate tokens, or implement token exchange)
- Caching / rate-limit: Redis (recommended) or in-memory for low-volume
- Optional: Celery / RQ for long-running tasks (image prefetching, scraping)

Environment variables (backend)
- DATABASE_URL — Neon Postgres connection string
- SECRET_KEY — app secret for signing tokens if used
- OPENAI_API_KEY or GROK_API_KEY — LLM provider keys
- MCP_APIFY_AUTH_HEADER — header value for apify mcp remote
- PEXELS_API_KEY — if Pexels direct usage is necessary
- BETTER_AUTH_SECRET / CLIENT_ID — BetterAuth integration values
- REDIS_URL — if using Redis
- ALLOWED_ORIGINS — CORS

API contract (recommended)
- Auth
  - POST /api/auth/signup
  - POST /api/auth/login
  - POST /api/auth/logout
  - GET /api/auth/me
- Places & Chat
  - POST /api/places  -> body {query} -> {placeData, imageUrls}
  - POST /api/chat/start -> {sessionId}
  - POST /api/chat/{sessionId}/message -> {message, streaming?}
  - GET /api/chat/{sessionId}/messages
  - GET /api/chat/sessions -> list
  - DELETE /api/chat/{sessionId} -> deletes session (GDPR/CCPA)
  - GET /api/export/user/{userId} -> export personal data (GDPR/CCPA)

Data models (summary)
- User: id, email, display_name, hashed_password, created_at, consent_flags
- Session: id, user_id, title, created_at, updated_at
- Message: id, session_id, role (user/assistant/tool), content, metadata (tool outputs)
- Place: cached record for frequent queries (id, name, geo, description, source, images)

Agent flow (backend)
4. Agent composes answer via litellm -> grok model and returns structured JSON (text + images + sources)
5. Persist session and messages

Persistence & retention
- Cache/store images returned by MCP in object storage (S3) or in a dedicated image CDN cache
- Implement a background purge job that deletes chat/session records older than 30 days (configurable)

1. Receive user query for a place
2. Check cache / DB for existing Place entry
3. If not available or stale, agent invokes MCP tools:
   - Apify MCP: scrape authoritative descriptions and facts
   - Pexels MCP: search images (or return curated image URLs)
4. Agent composes answer via litellm -> grok model and returns structured JSON (text + images + sources)
5. Persist session and messages

Compliance & privacy features (must implement)
- Store minimal PII and track user consent flags
- Provide endpoints for data export and deletion
- Keep audit logs (who requested deletion/export)
- Provide retention policy config and automation

Security & deployment notes
- Use HTTPS/TLS in production
- Restrict MCP keys and do not expose them to frontend
- Rate-limit endpoints and agent tool calls
- Sanitize any scraped content before returning to user

Compatibility and potential issues
- Verify that the OpenAI Agents SDK + litellm supports the specific Grok model you want (grok-3-fast / grok-3-mini) and that you have access/credentials
- `pexels-mcp-server` must be compatible with your Python environment; check versions
- Apify mcp-remote uses `npx` and Node tooling; for server-side automation prefer a backend proxy or scheduled scraping service
- Neon works with asyncpg; use async DB drivers and connection pooling to avoid timeouts under load

Questions / gaps (see also resources file)
- Confirm which LLM provider and model (grok-3-fast vs grok-3-mini) and where API keys come from
- How will MCP auth header for Apify be provided securely? (env or secrets manager)
- Should images be stored/cached or only proxied?
- Do you require real-time streaming into the frontend (SSE/WebSocket)?
