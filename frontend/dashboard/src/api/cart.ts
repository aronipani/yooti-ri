import axios from 'axios'
import type { Cart } from '../types/cart'

const api = axios.create({ baseURL: '/api/v1/cart' })

export async function getCart(): Promise<Cart> {
  const { data } = await api.get<Cart>('')
  return data
}

export async function addToCart(productId: string, quantity: number = 1): Promise<Cart> {
  const { data } = await api.post<Cart>('/items', { product_id: productId, quantity })
  return data
}

export async function updateCartItem(productId: string, quantity: number): Promise<Cart> {
  const { data } = await api.put<Cart>(`/items/${productId}`, { quantity })
  return data
}

export async function removeCartItem(productId: string): Promise<Cart> {
  const { data } = await api.delete<Cart>(`/items/${productId}`)
  return data
}
