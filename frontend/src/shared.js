export const CATEGORIES = ['Sedan', 'SUV', 'Truck', 'Hatchback', 'Coupe', 'Electric', 'Van']

export const EMPTY_FILTERS = { make: '', model: '', category: '', min_price: '', max_price: '' }

export const CATEGORY_ICONS = {
  sedan: '🚗', suv: '🚙', truck: '🛻', hatchback: '🚘', coupe: '🏎️', electric: '⚡', van: '🚐',
}

const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })
export const formatPrice = (value) => money.format(value)
