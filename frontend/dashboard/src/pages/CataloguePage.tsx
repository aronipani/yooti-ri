import { useEffect, useRef, useState, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getCategories } from '../api/products'
import { useProducts } from '../hooks/useProducts'
import { useCart } from '../contexts/CartContext'
import { ProductGrid } from '../components/ProductGrid'
import { SearchBar } from '../components/SearchBar'
import type { Category, ProductListItem } from '../types/product'

export function CataloguePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [categories, setCategories] = useState<Category[]>([])
  const [searchResults, setSearchResults] = useState<ProductListItem[] | null>(null)
  const [searchTotal, setSearchTotal] = useState(0)
  const sentinelRef = useRef<HTMLDivElement>(null)

  const category = searchParams.get('category') ?? undefined
  const sort = searchParams.get('sort') ?? undefined

  const { products, isLoading, hasNext, loadMore, total } = useProducts({ category, sort })
  const { addItem } = useCart()

  const isSearchActive = searchResults !== null

  useEffect(() => {
    void getCategories().then(setCategories)
  }, [])

  // IntersectionObserver for infinite scroll
  useEffect(() => {
    const sentinel = sentinelRef.current
    if (!sentinel) return

    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting && hasNext && !isLoading) {
          loadMore()
        }
      },
      { rootMargin: '200px' }
    )
    observer.observe(sentinel)
    return () => observer.disconnect()
  }, [hasNext, isLoading, loadMore])

  const handleCategoryChange = useCallback(
    (slug: string) => {
      const params = new URLSearchParams(searchParams)
      if (slug) {
        params.set('category', slug)
      } else {
        params.delete('category')
      }
      setSearchParams(params)
    },
    [searchParams, setSearchParams]
  )

  const handleSortChange = useCallback(
    (value: string) => {
      const params = new URLSearchParams(searchParams)
      if (value) {
        params.set('sort', value)
      } else {
        params.delete('sort')
      }
      setSearchParams(params)
    },
    [searchParams, setSearchParams]
  )

  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Products</h1>

      <SearchBar
        onResults={(items, resultTotal) => {
          setSearchResults(items)
          setSearchTotal(resultTotal)
        }}
        onClear={() => {
          setSearchResults(null)
          setSearchTotal(0)
        }}
      />

      {isSearchActive ? (
        <>
          <p className="text-sm text-gray-500 mb-4">{searchTotal} search results</p>
          <ProductGrid products={searchResults} onAddToCart={addItem} />
        </>
      ) : (
        <>
      <div className="flex gap-4 mb-6">
        <label className="flex items-center gap-2">
          Category:
          <select
            value={category ?? ''}
            onChange={e => handleCategoryChange(e.target.value)}
            className="border rounded px-2 py-1"
          >
            <option value="">All</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.slug}>
                {cat.name}
              </option>
            ))}
          </select>
        </label>

        <label className="flex items-center gap-2">
          Sort:
          <select
            value={sort ?? ''}
            onChange={e => handleSortChange(e.target.value)}
            className="border rounded px-2 py-1"
          >
            <option value="">Default</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
          </select>
        </label>
      </div>

      <p className="text-sm text-gray-500 mb-4">{total} products</p>

      <ProductGrid products={products} onAddToCart={addItem} />

      {isLoading && <p className="text-center py-4">Loading...</p>}

      <div ref={sentinelRef} aria-hidden="true" />
        </>
      )}
    </main>
  )
}
