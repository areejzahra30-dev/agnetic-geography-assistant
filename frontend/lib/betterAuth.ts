const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export async function login(email: string, password: string) {
  const res = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) return null
  try {
    return await res.json()
  } catch {
    return null
  }
}

export async function signup(email: string, password: string) {
  const res = await fetch(`${BASE}/api/auth/signup`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) throw new Error('Signup failed')
  return res.json()
}

export async function logout() {
  await fetch(`${BASE}/api/auth/logout`, { method: 'POST', credentials: 'include' })
}

export async function getCurrentUser() {
  const res = await fetch(`${BASE}/api/auth/me`, { credentials: 'include' })
  if (!res.ok) return null
  return res.json()
}
