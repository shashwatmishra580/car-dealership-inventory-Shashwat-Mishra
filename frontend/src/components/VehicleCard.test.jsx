import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import VehicleCard from './VehicleCard'

const car = { id: 1, make: 'Toyota', model: 'Camry', category: 'Sedan', price: 28000, quantity: 3 }

test('purchase button is enabled when in stock and calls back', async () => {
  const onPurchase = vi.fn()
  render(<VehicleCard vehicle={car} onPurchase={onPurchase} />)
  const button = screen.getByRole('button', { name: /purchase/i })
  expect(button).toBeEnabled()
  await userEvent.click(button)
  expect(onPurchase).toHaveBeenCalledWith(car)
})

test('purchase button is disabled and badge shown when out of stock', () => {
  render(<VehicleCard vehicle={{ ...car, quantity: 0 }} onPurchase={() => {}} />)
  expect(screen.getByRole('button', { name: /purchase/i })).toBeDisabled()
  expect(screen.getByText(/out of stock/i)).toBeInTheDocument()
})

test('admin controls are hidden from regular users', () => {
  render(<VehicleCard vehicle={car} isAdmin={false} onPurchase={() => {}} />)
  expect(screen.queryByRole('button', { name: /delete/i })).not.toBeInTheDocument()
  expect(screen.queryByRole('button', { name: /edit/i })).not.toBeInTheDocument()
})

test('admins can edit, delete and restock', () => {
  render(<VehicleCard vehicle={car} isAdmin onPurchase={() => {}} />)
  expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /restock/i })).toBeInTheDocument()
})
