export interface CartItem {
  product_id: string
  product_name: string
  price: number
  quantity: number
  subtotal: number
  stock_warning: string | null
}

export interface Cart {
  items: CartItem[]
  subtotal: number
  estimated_tax: number
  total: number
  item_count: number
}
