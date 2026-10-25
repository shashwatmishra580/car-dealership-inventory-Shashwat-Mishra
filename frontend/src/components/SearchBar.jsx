import { CATEGORIES, EMPTY_FILTERS } from '../shared'

const field =
  'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200'

export default function SearchBar({ filters, onChange }) {
  const set = (key) => (e) => onChange({ ...filters, [key]: e.target.value })
  const hasFilters = Object.values(filters).some(Boolean)

  return (
    <section
      aria-label="Search vehicles"
      className="grid gap-3 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200 sm:grid-cols-2 lg:grid-cols-6"
    >
      <input aria-label="Make" placeholder="Make" value={filters.make} onChange={set('make')} className={field} />
      <input aria-label="Model" placeholder="Model" value={filters.model} onChange={set('model')} className={field} />
      <select aria-label="Category" value={filters.category} onChange={set('category')} className={field}>
        <option value="">All categories</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
      <input aria-label="Min price" type="number" min="0" placeholder="Min price" value={filters.min_price} onChange={set('min_price')} className={field} />
      <input aria-label="Max price" type="number" min="0" placeholder="Max price" value={filters.max_price} onChange={set('max_price')} className={field} />
      <button
        type="button"
        disabled={!hasFilters}
        onClick={() => onChange(EMPTY_FILTERS)}
        className="rounded-xl border border-slate-300 px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 disabled:opacity-40"
      >
        Clear filters
      </button>
    </section>
  )
}
