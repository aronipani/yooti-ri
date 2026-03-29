import type { ProductListItem } from '../types/product'
import { ProductCard } from './ProductCard'

interface ProductGridProps {
  products: ProductListItem[]
  onAddToCart?: (productId: string) => void
}

export function ProductGrid({ products, onAddToCart }: ProductGridProps) {
  if (products.length === 0) {
    return <p className="text-center text-gray-500 py-8">No products found.</p>
  }

  return (
    <div
      className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
      role="list"
    >
      {products.map(product => (
        <div key={product.id} role="listitem">
          <ProductCard product={product} onAddToCart={onAddToCart} />
        </div>
      ))}
    </div>
  )
}
