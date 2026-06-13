Resources & Compliance — links, tools, and GDPR/CCPA checklist

Key resources
- Next.js: https://nextjs.org/
- FastAPI: https://fastapi.tiangolo.com/
- BetterAuth docs: https://better-auth.com/docs/installation
- shadcn/ui: https://ui.shadcn.com/
- KokonutUI ai-input-search: (via shadcn/registry or npm)
- OpenAI Agents SDK (Python): check official OpenAI Python SDK and agents docs
- litellm: https://pypi.org/project/litellm/ and docs for configuring Grok models
- Apify MCP remote: `npx mcp-remote https://mcp.apify.com/` (see Apify docs for API and auth)
- Pexels MCP server (pip): pexels-mcp-server (pip package)
- Neon Postgres: https://neon.tech/

- Consent & transparency: show clear privacy notice and cookie/consent banner
- Data minimization: only store necessary PII
- Data export: endpoint to export user data (JSON) on request
- Data deletion: endpoint to delete user data and sessions
- Retention policy: configurable retention and automated purge
- Lawful basis: record user's consent or other legal basis
- Third-party contracts: review and record DPA with third-party processors (OpenAI, Apify, Pexels, Neon)
- Data security: TLS in transit, encrypted backups at rest where possible
- Access controls & logging: admin-only access to raw PII and retention of logs per policy

GDPR & CCPA checklist (minimum)
- Consent & transparency: show clear privacy notice and cookie/consent banner
- Data minimization: only store necessary PII (email, display name)
- Data export: endpoint to export user data (JSON) on request
- Data deletion: endpoint to delete user data and sessions
- Retention policy: default 30 days for chat/session data (implement purge job and allow user-initiated deletion)
- Lawful basis: record user's consent or other legal basis
- Third-party contracts: review and record DPA with third-party processors (OpenAI, Apify, Pexels, Neon)
- Data security: TLS in transit, encrypted backups at rest where possible
- Access controls & logging: admin-only access to raw PII and retention of logs per policy

Notes about auth/no-email-verification
- You requested email + password auth with NO email verification. This is allowed but increases the risk of account hijacking and makes proving identity for deletion/export requests harder. Consider adding optional account-recovery flows (password reset via email) and strong password rules.

- Consent & transparency: show clear privacy notice and cookie/consent banner
- Data minimization: only store necessary PII
- Data export: endpoint to export user data (JSON) on request
- Data deletion: endpoint to delete user data and sessions
- Retention policy: configurable retention and automated purge
- Lawful basis: record user's consent or other legal basis
- Third-party contracts: review and record DPA with third-party processors (OpenAI, Apify, Pexels, Neon)
- Data security: TLS in transit, encrypted backups at rest where possible
- Access controls & logging: admin-only access to raw PII and retention of logs per policy

Recommended libraries & tools
- SQLModel / SQLAlchemy (async) + Alembic for migrations
- asyncpg for Neon
- Redis for rate-limiting and cache
- Sentry or similar for error monitoring (privacy-aware)

Deployment recommendations
- Host backend on a platform that supports long-running ASGI workers (Fly, Render, DigitalOcean App Platform, or self-managed)
- Host Next.js on a platform with good support for streaming if needed (Vercel has restrictions for SSE)
- Use a secrets manager (AWS Secrets Manager, Vault, or platform secrets)

Permissions & keys
- Never commit keys to repo. Use `.env` locally and secrets in CI
- MCP Apify requires header-defined auth; ensure backend stores this secret and uses it server-side

Questions / gaps to confirm
- Which exact LLM provider and model will be used (grok-3-fast vs grok-3-mini) and do you already have access keys?
- Do you want images cached on the backend or proxied directly from Pexels/Apify results?
- Is streaming (progressive assistant output) required in the UI?
- Are social sign-ins required (Google/GitHub)?
- Do you plan to allow user uploads (images) or only sourced images?
- Which hosting/production domain will be used (for CORS and cookie config)?

Next actions I can take
- Implement a minimal FastAPI skeleton with example agent route
- Add DB models and Alembic migrations
- Scaffold Next.js pages and the `ai-input-search` component
- Wire BetterAuth quickstart for auth flow
