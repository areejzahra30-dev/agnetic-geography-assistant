# Agentic Geography Assistant — Frontend Example

This folder contains a minimal Next.js example to demonstrate the AI input search, BetterAuth wiring, and an SSE streaming client that listens for assistant messages and images.

Quick start

1. Install dependencies
```bash
cd frontend
npm install
```

2. Add env
Copy `.env.example` to `.env.local` and adjust `NEXT_PUBLIC_API_BASE_URL` if needed.

3. Run dev server
```bash
npm run dev
```

How it works
- `pages/index.tsx` contains a demo UI with `AIInput` and an SSE client that connects to `${NEXT_PUBLIC_API_BASE_URL}/api/stream` with a `sessionId` query.
- `lib/betterAuth.ts` contains lightweight wrappers for auth endpoints (`/api/auth/*`) and assumes the backend sets HTTP-only cookies for session tokens.

Notes
- Replace the `@kokonutui/ai-input-search` usage or install it via `npm` if you want the exact component.
- Backend endpoints expected:
  - `POST /api/chat/start` -> { sessionId }
  - `GET /api/stream?sessionId=...` -> SSE streaming messages (JSON events) with fields `{type: 'message'|'image', text?, url?}`
  - `POST /api/auth/login`, `POST /api/auth/signup`, `POST /api/auth/logout`, `GET /api/auth/me`
