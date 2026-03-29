import { useCallback, useEffect, useRef, useState } from 'react'
import { getProducts, type GetProductsParams } from '../api/products'
import type { ProductListItem } from '../types/product'

interface UseProductsOptions {
  category?: string
  sort?: string
  limit?: number
}

interface UseProductsResult {
  products: ProductListItem[]
  isLoading: boolean
  hasNext: boolean
  loadMore: () => void
  total: number
}

export function useProducts(options: UseProductsOptions = {}): UseProductsResult {
  const [products, setProducts] = useState<ProductListItem[]>([])
  const [page, setPage] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [hasNext, setHasNext] = useState(false)
  const [total, setTotal] = useState(0)
  const prevKey = useRef('')

  const key = `${options.category ?? ''}-${options.sort ?? ''}`

  useEffect(() => {
    if (key !== prevKey.current) {
      setProducts([])
      setPage(1)
      prevKey.current = key
    }
  }, [key])

  useEffect(() => {
    let cancelled = false
    const fetchData = async () => {
      setIsLoading(true)
      try {
        const params: GetProductsParams = {
          page,
          limit: options.limit ?? 20,
        }
        if (options.category) params.category = options.category
        if (options.sort) params.sort = options.sort

        const result = await getProducts(params)
        if (!cancelled) {
          setProducts(prev => page === 1 ? result.items : [...prev, ...result.items])
          setHasNext(result.has_next)
          setTotal(result.total)
        }
      } finally {
        if (!cancelled) setIsLoading(false)
      }
    }
    void fetchData()
    return () => { cancelled = true }
  }, [page, options.category, options.sort, options.limit])

  const loadMore = useCallback(() => {
    if (!isLoading && hasNext) {
      setPage(p => p + 1)
    }
  }, [isLoading, hasNext])

  return { products, isLoading, hasNext, loadMore, total }
}
