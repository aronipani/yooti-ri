import { useEffect, useState } from 'react'
import { getProductById } from '../api/products'
import type { ProductDetail } from '../types/product'

interface UseProductResult {
  product: ProductDetail | null
  isLoading: boolean
  isNotFound: boolean
}

export function useProduct(id: string): UseProductResult {
  const [product, setProduct] = useState<ProductDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isNotFound, setIsNotFound] = useState(false)

  useEffect(() => {
    let cancelled = false
    const fetch = async () => {
      setIsLoading(true)
      setIsNotFound(false)
      try {
        const data = await getProductById(id)
        if (!cancelled) setProduct(data)
      } catch {
        if (!cancelled) setIsNotFound(true)
      } finally {
        if (!cancelled) setIsLoading(false)
      }
    }
    void fetch()
    return () => { cancelled = true }
  }, [id])

  return { product, isLoading, isNotFound }
}
