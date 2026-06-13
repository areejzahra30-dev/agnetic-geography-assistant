Front-end Requirements — Agentic Geography Assistant

Purpose: provide a Next.js (latest) frontend that interacts with the backend FastAPI agent service to let users ask about places (city/state/country), view answers and related images, and manage user profile and sessions.

Chosen configuration (from user)
- LLM model: `grok-3-fast` (backend provides answers)
- Images: served by backend (cached/stored on backend)
- Streaming: frontend must support progressive streaming of assistant responses (SSE or WebSocket)
- Auth: email + password only, NO email verification
- Hosting: frontend planned for Vercel or Netlify; backend on Render or Railway; configure CORS to allow `http://localhost:3000`, `https://app.domain.com`, and `https://api.domain.com` (adjust to your final domains)


Core goals
- Fast, accessible UI for text queries and image display
- Authentication for users (sign up/sign in/logout/profile)
- Session/chat history listing and retrieval
- Error handling, rate-limit UX, and privacy controls for GDPR/CCPA

Tech stack
- Framework: Next.js (latest) — prefer App Router (React Server Components) or Pages as you prefer
- Runtime: Bun or Node (user prefers Bun commands shown in setup)
- UI: shadcn/ui components + @kokonutui/ai-input-search for the input component
- Auth: BetterAuth frontend SDK (see BetterAuth docs)
- HTTP: fetch / axios for API calls, use `SSE` or `EventSource` for streaming responses if implemented in backend

Frontend responsibilities (contract with backend)
- Auth flows: call backend endpoints for sign-in/sign-up and exchange tokens (BetterAuth + backend validation)
- Request place info: GET /api/places?query=<q> or POST /api/places with body {query}
- Chat/session management:
  - POST /api/chat/start -> {sessionId}
  - POST /api/chat/{sessionId}/message -> {message}
  - GET /api/chat/{sessionId}/messages
  - DELETE /api/chat/{sessionId} (for GDPR/CCPA deletion)
- Image fetch: backend returns image URLs (backend caches/stores images); frontend displays cached images

- NEXT_PUBLIC_API_BASE_URL — backend base URL
- NEXT_PUBLIC_AUTH_PROVIDER — BetterAuth config value if needed
- NEXT_PUBLIC_ANALYTICS_KEY (optional)

Production env variables
- NEXT_PUBLIC_API_BASE_URL=https://api.domain.com
- NEXT_PUBLIC_ALLOWED_ORIGINS=https://app.domain.com

- NEXT_PUBLIC_API_BASE_URL — backend base URL
- NEXT_PUBLIC_AUTH_PROVIDER — BetterAuth config value if needed
- NEXT_PUBLIC_ANALYTICS_KEY (optional)

Data & UI considerations
- Minimal personal data shown: display name, email (optionally), profile picture
- Show consent banner and privacy link on first visit
- Provide controls to delete/export chat history from UI (calls backend delete/export endpoints)

Performance & UX
- Cache place queries for short TTL (SWR or React Query) to reduce backend/MCP calls
- Use skeleton loading, graceful fallback images, lazy load images

Security
- Always use HTTPS in production
- Store tokens in secure cookies (HTTPOnly) or use BetterAuth recommended storage
- Validate and sanitize any user-provided query before sending to backend

Notes on compatibility
- Ensure SSE support if backend streams LLM responses; if deploying to Vercel confirm SSE support or use a streaming proxy
- Bun + Next.js: some node-native packages may require Node — maintain Node fallback for build/deps where necessary
