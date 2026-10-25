import { useState } from 'react'
import { getToken, parseToken, setToken } from './api'
import AuthForm from './components/AuthForm'
import Dashboard from './components/Dashboard'

export default function App() {
  const [token, setTokenState] = useState(getToken())
  const user = token ? parseToken(token) : null

  const handleLogin = (newToken) => {
    setToken(newToken)
    setTokenState(newToken)
  }
  const handleLogout = () => {
    setToken(null)
    setTokenState(null)
  }

  if (!user) return <AuthForm onLogin={handleLogin} />
  return <Dashboard user={user} onLogout={handleLogout} />
}
