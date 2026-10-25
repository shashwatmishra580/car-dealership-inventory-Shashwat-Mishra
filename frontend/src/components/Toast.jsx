export default function Toast({ toast }) {
  if (!toast) return null
  const color = toast.type === 'error' ? 'bg-rose-600' : 'bg-emerald-600'
  return (
    <div
      role="status"
      className={`fixed bottom-6 right-6 z-50 rounded-xl px-5 py-3 text-sm font-medium text-white shadow-xl ${color}`}
    >
      {toast.message}
    </div>
  )
}
