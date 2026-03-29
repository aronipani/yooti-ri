import axios from 'axios'
import type { PaginatedResponse, Category, ProductDetail } from '../types/product'

const api = axios.create({ baseURL: '/api/v1' })

export interface GetProductsParams {
  category?: string
  sort?: string
  page?: number
  limit?: number
}

export async function getProducts(params: GetProductsParams = {}): Promise<PaginatedResponse> {
  const { data } = await api.get<PaginatedResponse>('/products', { params })
  return data
}

export async function getCategories(): Promise<Category[]> {
  const { data } = await api.get<Category[]>('/categories')
  return data
}

export async function getProductById(id: string): Promise<ProductDetail> {
  const { data } = await api.get<ProductDetail>(`/products/${id}`)
  return data
}
