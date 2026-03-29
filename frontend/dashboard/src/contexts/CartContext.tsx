import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'
import type { Cart } from '../types/cart'
import * as cartApi from '../api/cart'

interface CartContextValue {
  cart: Cart
  isOpen: boolean
  openCart: () => void
  closeCart: () => void
  addItem: (productId: string, quantity?: number) => Promise<void>
  updateItem: (productId: string, quantity: number) => Promise<void>
  removeItem: (productId: string) => Promise<void>
  refreshCart: () => Promise<void>
}

const emptyCart: Cart = { items: [], subtotal: 0, estimated_tax: 0, total: 0, item_count: 0 }

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart>(emptyCart)
  const [isOpen, setIsOpen] = useState(false)

  const refreshCart = useCallback(async () => {
    try {
      const data = await cartApi.getCart()
      setCart(data)
    } catch {
      // Cart may not exist yet
    }
  }, [])

  const addItem = useCallback(async (productId: string, quantity: number = 1) => {
    const updated = await cartApi.addToCart(productId, quantity)
    setCart(updated)
    setIsOpen(true)
  }, [])

  const updateItem = useCallback(async (productId: string, quantity: number) => {
    const updated = await cartApi.updateCartItem(productId, quantity)
    setCart(updated)
  }, [])

  const removeItem = useCallback(async (productId: string) => {
    const updated = await cartApi.removeCartItem(productId)
    setCart(updated)
  }, [])

  const openCart = useCallback(() => setIsOpen(true), [])
  const closeCart = useCallback(() => setIsOpen(false), [])

  const value = useMemo(
    () => ({ cart, isOpen, openCart, closeCart, addItem, updateItem, removeItem, refreshCart }),
    [cart, isOpen, openCart, closeCart, addItem, updateItem, removeItem, refreshCart]
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used within CartProvider')
  return ctx
}
