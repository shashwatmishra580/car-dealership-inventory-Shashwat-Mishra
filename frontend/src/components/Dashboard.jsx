import { useEffect, useState } from 'react'
import { api } from '../api'
import { EMPTY_FILTERS } from '../shared'
import SearchBar from './SearchBar'
import Toast from './Toast'
import VehicleCard from './VehicleCard'
import VehicleForm from './VehicleForm'

/** Delays a fast-changing value (search filters) so we don't call the API on every keystroke. */
function useDebounced(value, delay = 300) {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  return debounced
}

export default function Dashboard({ user, onLogout }) {
  const isAdmin = user.role === 'ADMIN'
  const [vehicles, setVehicles] = useState([])
  const [filters, setFilters] = useState(EMPTY_FILTERS)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(null) // null | 'new' | a vehicle object
  const [toast, setToast] = useState(null)
  const [reloadKey, setReloadKey] = useState(0)
  const debouncedFilters = useDebounced(filters)

  const notify = (type, message) => {
    setToast({ type, message })
    setTimeout(() => setToast(null), 3000)
  }
  const reload = () => setReloadKey((k) => k + 1)
  // An expired/invalid token sends the user back to the login screen.
  const handleError = (err) => (err.status === 401 ? onLogout() : notify('error', err.message))

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    api
      .searchVehicles(debouncedFilters)
      .then((data) => {
        if (cancelled) return
        setVehicles(data)
        setError('')
      })
      .catch((err) => {
        if (cancelled) return
        if (err.status === 401) onLogout()
        else setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [debouncedFilters, reloadKey])

  const replace = (updated) => setVehicles((list) => list.map((v) => (v.id === updated.id ? updated : v)))

  const purchase = async (vehicle) => {
    try {
      const updated = await api.purchase(vehicle.id)
      replace(updated)
      notify('success', `You purchased a ${updated.make} ${updated.model}!`)
    } catch (err) {
      handleError(err)
      reload() // stock may have changed under us
    }
  }

  const restock = async (vehicle, amount) => {
    try {
      const updated = await api.restock(vehicle.id, amount)
      replace(updated)
      notify('success', `Restocked ${updated.make} ${updated.model} (+${amount})`)
    } catch (err) {
      handleError(err)
    }
  }

  const remove = async (vehicle) => {
    if (!window.confirm(`Delete ${vehicle.make} ${vehicle.model}?`)) return
    try {
      await api.removeVehicle(vehicle.id)
      setVehicles((list) => list.filter((v) => v.id !== vehicle.id))
      notify('success', 'Vehicle deleted')
    } catch (err) {
      handleError(err)
    }
  }

  const save = async (data) => {
    try {
      if (editing === 'new') await api.createVehicle(data)
      else await api.updateVehicle(editing.id, data)
      notify('success', editing === 'new' ? 'Vehicle added' : 'Vehicle updated')
      setEditing(null)
      reload()
    } catch (err) {
      handleError(err)
    }
  }

  const inStock = vehicles.filter((v) => v.quantity > 0).length
  const totalUnits = vehicles.reduce((sum, v) => sum + v.quantity, 0)

  return (
    <div className="min-h-screen">
      <header className="bg-gradient-to-r from-slate-900 via-indigo-900 to-violet-800 text-white">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-5 sm:px-6">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🚘</span>
            <div>
              <h1 className="text-xl font-bold">AutoVault</h1>
              <p className="text-xs text-indigo-200">Dealership inventory</p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden text-indigo-100 sm:inline">{user.email}</span>
            <span className="rounded-full bg-white/15 px-3 py-1 text-xs font-semibold">{user.role}</span>
            <button onClick={onLogout} className="rounded-xl bg-white/10 px-4 py-2 font-medium hover:bg-white/20">
              Log out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6">
        <div className="grid gap-4 sm:grid-cols-3">
          {[
            ['Models listed', vehicles.length],
            ['Models in stock', inStock],
            ['Total units', totalUnits],
          ].map(([label, value]) => (
            <div key={label} className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
              <p className="text-sm text-slate-500">{label}</p>
              <p className="text-3xl font-extrabold text-slate-900">{value}</p>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-slate-900">Available vehicles</h2>
          {isAdmin && (
            <button
              onClick={() => setEditing('new')}
              className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow hover:bg-indigo-700"
            >
              + Add vehicle
            </button>
          )}
        </div>

        <SearchBar filters={filters} onChange={setFilters} />

        {error ? (
          <p role="alert" className="rounded-xl bg-rose-50 p-4 text-rose-700">{error}</p>
        ) : loading ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-80 animate-pulse rounded-2xl bg-slate-200" />
            ))}
          </div>
        ) : vehicles.length === 0 ? (
          <div className="rounded-2xl border-2 border-dashed border-slate-300 p-12 text-center text-slate-500">
            <p className="text-4xl">🔍</p>
            <p className="mt-2 font-medium">No vehicles match your search.</p>
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {vehicles.map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                isAdmin={isAdmin}
                onPurchase={purchase}
                onRestock={restock}
                onEdit={setEditing}
                onDelete={remove}
              />
            ))}
          </div>
        )}
      </main>

      {editing && (
        <VehicleForm vehicle={editing === 'new' ? null : editing} onSave={save} onClose={() => setEditing(null)} />
      )}
      <Toast toast={toast} />
    </div>
  )
}
