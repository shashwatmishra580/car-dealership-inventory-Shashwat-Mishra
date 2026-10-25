import { useState } from 'react'
import { CATEGORY_ICONS, formatPrice } from '../shared'

/** One vehicle: stock badges, purchase button, and (for admins) edit/delete/restock controls. */
export default function VehicleCard({ vehicle, isAdmin = false, onPurchase, onEdit, onDelete, onRestock }) {
  const [restockAmount, setRestockAmount] = useState(5)
  const soldOut = vehicle.quantity === 0
  const lowStock = !soldOut && vehicle.quantity <= 2
  const icon = CATEGORY_ICONS[vehicle.category.toLowerCase()] ?? '🚗'

  return (
    <article className="flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-200 transition hover:-translate-y-1 hover:shadow-lg">
      <div className="relative flex h-36 items-center justify-center bg-gradient-to-br from-indigo-100 via-sky-50 to-violet-100 text-6xl">
        <span aria-hidden="true">{icon}</span>
        <span className="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-indigo-700">
          {vehicle.category}
        </span>
        {soldOut && (
          <span className="absolute right-3 top-3 rounded-full bg-rose-600 px-3 py-1 text-xs font-semibold text-white">
            Out of stock
          </span>
        )}
        {lowStock && (
          <span className="absolute right-3 top-3 rounded-full bg-amber-500 px-3 py-1 text-xs font-semibold text-white">
            Only {vehicle.quantity} left
          </span>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-3 p-5">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{vehicle.make}</p>
          <h3 className="text-lg font-bold text-slate-900">{vehicle.model}</h3>
        </div>
        <div className="flex items-end justify-between">
          <p className="text-2xl font-extrabold text-indigo-600">{formatPrice(vehicle.price)}</p>
          <p className="text-sm text-slate-500">{vehicle.quantity} in stock</p>
        </div>

        <button
          type="button"
          disabled={soldOut}
          onClick={() => onPurchase(vehicle)}
          className="mt-auto rounded-xl bg-indigo-600 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          Purchase
        </button>

        {isAdmin && (
          <div className="space-y-2 border-t border-slate-100 pt-3">
            <div className="flex gap-2">
              <input
                type="number"
                min="1"
                aria-label="Restock amount"
                value={restockAmount}
                onChange={(e) => setRestockAmount(e.target.value)}
                className="w-20 rounded-lg border border-slate-300 px-2 py-1.5 text-sm"
              />
              <button
                type="button"
                onClick={() => onRestock(vehicle, Number(restockAmount))}
                className="flex-1 rounded-lg bg-emerald-50 px-3 py-1.5 text-sm font-medium text-emerald-700 hover:bg-emerald-100"
              >
                Restock
              </button>
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => onEdit(vehicle)}
                className="flex-1 rounded-lg bg-slate-100 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-200"
              >
                Edit
              </button>
              <button
                type="button"
                onClick={() => onDelete(vehicle)}
                className="flex-1 rounded-lg bg-rose-50 px-3 py-1.5 text-sm font-medium text-rose-700 hover:bg-rose-100"
              >
                Delete
              </button>
            </div>
          </div>
        )}
      </div>
    </article>
  )
}
