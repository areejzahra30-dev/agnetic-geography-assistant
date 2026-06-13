Frontend Setup — Next.js (Bun/Node) quickstart

Prerequisites
- Install Bun (optional) or Node.js (v18+)
- git

Create project (Next.js latest)
Using Bun (recommended if you prefer bun commands):
```bash
bun create next ./app
cd app
```
Using npm:
```bash
npx create-next-app@latest app
cd app
```

Install UI + input component
```bash
# shadcn base (example)
bunx --bun shadcn@latest add @kokonutui/ai-input-search
# or with npm/yarn
npx shadcn-ui add @kokonutui/ai-input-search
```

Install essential packages
```bash
bun add axios swr clsx tailwindcss@latest postcss autoprefixer
# or npm/yarn equivalents
```

BetterAuth integration
- Follow BetterAuth docs: https://better-auth.com/docs/installation
- Add frontend SDK config and point to backend auth endpoints
- Optionally run `npx skills add better-auth/skills` for their recommended setup snippets

Env and run
- Create `.env.local` with:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_PROVIDER=better-auth-provider-id
```
- Start dev server
```bash
bun dev # or npm run dev
```

Production & hosting notes
- Hosting: frontend planned for Vercel or Netlify; backend will be on Render/Railway (`api.domain.com`).
- Set production envs in Vercel/Netlify with:
```
NEXT_PUBLIC_API_BASE_URL=https://api.domain.com
NEXT_PUBLIC_ALLOWED_ORIGINS=https://app.domain.com
```
- Streaming caveat: Vercel/Netlify frontend hosting is fine, but streaming from serverless functions can be limited. Because your backend is on Render/Railway (long-running ASGI), SSE from `https://api.domain.com` to the frontend is acceptable. If you prefer maximum compatibility, implement WebSocket fallback for progressive streaming.


Auth UX & storage
- Use BetterAuth recommended storage or secure cookies
- Use server-side sessions if you prefer stronger token handling

Notes
- The frontend should call backend API endpoints for place queries and receive image URLs rather than direct image API keys
- For streaming agent responses, use `EventSource` if backend exposes SSE
