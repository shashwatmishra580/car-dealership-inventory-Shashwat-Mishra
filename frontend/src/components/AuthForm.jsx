import { useState } from 'react'
import { api } from '../api'

const field =
  'mt-1 w-full rounded-xl border border-slate-300 px-4 py-2.5 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200'

/** Login / register form. Registering signs the user in straight away. */
export default function AuthForm({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const isLogin = mode === 'login'

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (!isLogin) await api.register(form)
      const { access_token } = await api.login(form)
      onLogin(access_token)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-violet-800 p-4">
      <div className="w-full max-w-md rounded-3xl bg-white/95 p-8 shadow-2xl">
        <div className="mb-6 text-center">
          <div className="text-5xl">🚘</div>
          <h1 className="mt-2 text-2xl font-bold text-slate-900">AutoVault</h1>
          <p className="text-sm text-slate-500">{isLogin ? 'Sign in to manage inventory' : 'Create your account'}</p>
        </div>

        <form onSubmit={submit} className="space-y-4">
          <label className="block text-sm font-medium text-slate-700">
            Email
            <input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className={field} />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Password
            <input type="password" required minLength={isLogin ? 1 : 8} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className={field} />
          </label>
          {error && (
            <p role="alert" className="rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">
              {error}
            </p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-indigo-600 py-2.5 font-semibold text-white transition hover:bg-indigo-700 disabled:opacity-60"
          >
            {loading ? 'Please wait…' : isLogin ? 'Sign in' : 'Create account'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-500">
          {isLogin ? "Don't have an account?" : 'Already registered?'}{' '}
          <button
            type="button"
            onClick={() => {
              setMode(isLogin ? 'register' : 'login')
              setError('')
            }}
            className="font-semibold text-indigo-600 hover:underline"
          >
            {isLogin ? 'Register' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  )
}
