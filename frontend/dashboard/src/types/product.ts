export interface ProductListItem {
  id: string
  name: string
  price: number
  thumbnail_url: string | null
  stock_quantity: number
  stock_status: 'in_stock' | 'out_of_stock'
  category_slug: string
}

export interface Category {
  id: string
  name: string
  slug: string
}

export interface PaginatedResponse {
  items: ProductListItem[]
  total: number
  page: number
  limit: number
  has_next: boolean
}

export interface ProductDetail {
  id: string
  name: string
  description: string
  price: number
  stock_quantity: number
  stock_status: 'in_stock' | 'out_of_stock'
  thumbnail_url: string | null
  images: string[]
  category_name: string
  category_slug: string
}
