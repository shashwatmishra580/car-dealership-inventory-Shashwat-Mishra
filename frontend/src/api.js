// Thin wrapper around fetch: adds the JWT, parses errors into readable messages.
const TOKEN_KEY = 'autovault_token'

export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const setToken = (token) =>
  token ? localStorage.setItem(TOKEN_KEY, token) : localStorage.removeItem(TOKEN_KEY)

/** Decode the JWT payload (no verification: the server is the authority). */
export function parseToken(token) {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(payload))
  } catch {
    return null
  }
}

async function request(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`/api${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (response.status === 204) return null

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map((d) => d.msg).join(', ') : data.detail
    const error = new Error(detail || 'Something went wrong')
    error.status = response.status
    throw error
  }
  return data
}

export const api = {
  register: (credentials) => request('/auth/register', { method: 'POST', body: credentials }),
  login: (credentials) => request('/auth/login', { method: 'POST', body: credentials }),
  searchVehicles: (filters) => {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value != null) params.set(key, value)
    })
    const query = params.toString()
    return request(`/vehicles/search${query ? `?${query}` : ''}`)
  },
  createVehicle: (data) => request('/vehicles', { method: 'POST', body: data }),
  updateVehicle: (id, data) => request(`/vehicles/${id}`, { method: 'PUT', body: data }),
  removeVehicle: (id) => request(`/vehicles/${id}`, { method: 'DELETE' }),
  purchase: (id) => request(`/vehicles/${id}/purchase`, { method: 'POST' }),
  restock: (id, amount) => request(`/vehicles/${id}/restock`, { method: 'POST', body: { amount } }),
}
