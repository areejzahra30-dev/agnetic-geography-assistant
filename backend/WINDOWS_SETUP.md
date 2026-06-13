# Backend Setup Guide — Windows (psycopg2-binary)

This guide covers setting up the FastAPI backend on Windows using `psycopg2-binary` instead of `asyncpg`.

## Why psycopg2-binary?

- **No compiler needed**: Windows doesn't require a C compiler for database connections
- **Synchronous driver**: Simpler to debug and works out-of-the-box
- **SQLAlchemy compatible**: Works seamlessly with SQLAlchemy 2.0+
- **Production-ready**: Used in thousands of production deployments

## Prerequisites

- Python 3.11+ (check with `python --version`)
- pip (included with Python)
- Git (optional, for version control)

## Step 1: Create Virtual Environment

```powershell
# Open PowerShell in the backend folder
cd backend

# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# If you get a permission error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 2: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements (uses psycopg2-binary, not asyncpg)
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 psycopg2-binary-2.9.9 ...
```

## Step 3: Configure Environment

```powershell
# Copy example config
copy .env.example .env.local

# Edit .env.local with your settings (use Notepad or your editor)
# Minimum required:
# - GROK_API_KEY=your-grok-api-key (for live agent responses)
# 
# Optional (for production):
# - DATABASE_URL=postgresql+psycopg2://...
# - MCP_APIFY_HEADER=Authorization: ...
```

## Step 4: Run the Backend

```powershell
# Make sure you're in the backend folder and .venv is activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Visit `http://localhost:8000/docs` to see interactive API docs (Swagger UI).

## Step 5: Test the Agent & SSE Stream

In a new PowerShell window:

```powershell
cd backend

# Activate the same virtual environment
.venv\Scripts\Activate.ps1

# Run the direct agent test (no HTTP needed)
python test_agent.py "Tokyo"

# Or run HTTP endpoint tests (requires backend running)
python test_http_sse.py http://localhost:8000 "Paris"
```

## Step 6: Connect Frontend

In another PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` and test the full system.

## Troubleshooting

### Error: `No module named 'openai'`
**Solution:** Make sure `.venv` is activated and you ran `pip install -r requirements.txt`

### Error: `psycopg2.OperationalError: could not connect to server`
**Solution:** This is expected if Neon Postgres is not set up yet. The system works with in-memory storage locally. To use Neon:
1. Create a Neon account and cluster
2. Copy the connection string: `postgresql://user:password@host:5432/dbname`
3. Convert it to psycopg2 format: `postgresql+psycopg2://user:password@host:5432/dbname`
4. Set `DATABASE_URL` in `.env.local`

### Error: `GROK_API_KEY not set; using mock response`
**Solution:** This is normal and expected. The agent returns mock responses for testing. Set `GROK_API_KEY` in `.env.local` to use live responses.

### Port 8000 already in use
**Solution:** Change the port in the uvicorn command:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend can't reach backend (CORS error)
**Solution:** Update `ALLOWED_ORIGINS` in `.env.local`:
```
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Database Setup (Optional for Local Dev)

The system uses **in-memory session storage** by default (perfect for local testing).

To use **Neon Postgres**:

1. Create Neon account: https://neon.tech
2. Create a database cluster
3. Get connection string from Neon dashboard
4. Convert to psycopg2 format and set `DATABASE_URL`:
   ```powershell
   # Old format (don't use):
   # postgresql://user:pass@host/db
   
   # New format (psycopg2-binary):
   # postgresql+psycopg2://user:pass@host:5432/db
   ```

5. Run migrations to create tables:
   ```powershell
   # (When Alembic migrations are created)
   alembic upgrade head
   ```

## API Endpoints (Quick Reference)

- `GET /` — API info
- `GET /health` — Health check
- `GET /docs` — Interactive API docs (Swagger)
- `POST /api/auth/signup` — Register user
- `POST /api/auth/login` — Login user
- `POST /api/chat/start` — Start a chat session
- `GET /api/stream?sessionId=...` — SSE stream for agent responses

## Environment Variables Explained

```
GROK_API_KEY              # Grok LLM model API key (required for live responses)
MCP_APIFY_HEADER          # Apify MCP server auth header
PEXELS_API_KEY            # Pexels image search API key
DATABASE_URL              # Neon Postgres connection (optional for local dev)
SECRET_KEY                # Session/token signing key (change in production!)
ALLOWED_ORIGINS           # CORS origins (comma-separated)
SESSION_RETENTION_DAYS    # How long to keep chat history (default: 30)
IMAGE_CACHE_TTL_DAYS      # How long to cache images (default: 90)
```

## Windows Tips

- Use PowerShell or CMD (both work the same)
- File paths use `\` instead of `/` (psycopg2-binary handles this)
- `.venv\Scripts\Activate.ps1` activates the virtual environment
- `deactivate` command turns off the virtual environment
- Use `pip install` instead of `pip3 install` (Python 3 is default on Windows with latest installers)

## Next Steps

1. **Agent integration complete** ✅ — Ready to use grok-3-fast via litellm
2. **SSE streaming ready** ✅ — Progressive responses work
3. **Test scripts included** ✅ — Verify everything locally
4. **Production setup**:
   - Set up Neon Postgres and run Alembic migrations
   - Integrate real MCP tools (Apify, Pexels)
   - Deploy to Render/Railway (backend) and Vercel/Netlify (frontend)
   - Configure production secrets and CORS

Enjoy your agentic geography assistant! 🌍
