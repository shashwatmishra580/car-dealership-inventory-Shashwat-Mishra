import { useState } from 'react'
import { CATEGORIES } from '../shared'

const field =
  'mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200'

/** Modal used for both "Add vehicle" (vehicle = null) and "Edit vehicle". */
export default function VehicleForm({ vehicle, onSave, onClose }) {
  const [form, setForm] = useState({
    make: vehicle?.make ?? '',
    model: vehicle?.model ?? '',
    category: vehicle?.category ?? CATEGORIES[0],
    price: vehicle?.price ?? '',
    quantity: vehicle?.quantity ?? 0,
  })
  const [saving, setSaving] = useState(false)
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    await onSave({ ...form, price: Number(form.price), quantity: Number(form.quantity) })
    setSaving(false)
  }

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/60 p-4">
      <form
        role="dialog"
        aria-label={vehicle ? 'Edit vehicle' : 'Add vehicle'}
        onSubmit={submit}
        className="w-full max-w-md space-y-4 rounded-2xl bg-white p-6 shadow-2xl"
      >
        <h2 className="text-xl font-bold text-slate-900">{vehicle ? 'Edit vehicle' : 'Add vehicle'}</h2>
        <div className="grid grid-cols-2 gap-4">
          <label className="text-sm font-medium text-slate-700">
            Make
            <input required value={form.make} onChange={set('make')} className={field} />
          </label>
          <label className="text-sm font-medium text-slate-700">
            Model
            <input required value={form.model} onChange={set('model')} className={field} />
          </label>
        </div>
        <label className="block text-sm font-medium text-slate-700">
          Category
          <select value={form.category} onChange={set('category')} className={field}>
            {CATEGORIES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <div className="grid grid-cols-2 gap-4">
          <label className="text-sm font-medium text-slate-700">
            Price (USD)
            <input required type="number" min="1" step="any" value={form.price} onChange={set('price')} className={field} />
          </label>
          <label className="text-sm font-medium text-slate-700">
            Quantity
            <input required type="number" min="0" value={form.quantity} onChange={set('quantity')} className={field} />
          </label>
        </div>
        <div className="flex justify-end gap-3 pt-2">
          <button type="button" onClick={onClose} className="rounded-xl px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100">
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="rounded-xl bg-indigo-600 px-5 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60"
          >
            {saving ? 'Saving…' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  )
}
