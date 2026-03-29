import type { ProductListItem } from '../types/product'

interface ProductCardProps {
  product: ProductListItem
  onAddToCart?: (productId: string) => void
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const isOutOfStock = product.stock_status === 'out_of_stock'
  const formattedPrice = `$${Number(product.price).toFixed(2)}`

  return (
    <div
      className="product-card border rounded-lg p-4 flex flex-col"
      aria-label={`${product.name}, ${formattedPrice}, ${isOutOfStock ? 'out of stock' : 'in stock'}`}
    >
      {product.thumbnail_url ? (
        <img
          src={product.thumbnail_url}
          alt={product.name}
          className="w-full h-48 object-cover rounded"
        />
      ) : (
        <div className="w-full h-48 bg-gray-200 rounded flex items-center justify-center">
          <span className="text-gray-400">No image</span>
        </div>
      )}

      <h3 className="mt-2 font-semibold text-lg">{product.name}</h3>
      <p className="text-xl font-bold mt-1">{formattedPrice}</p>

      {isOutOfStock && (
        <span className="inline-block mt-1 px-2 py-1 bg-red-100 text-red-800 text-sm rounded">
          Out of Stock
        </span>
      )}

      <button
        type="button"
        disabled={isOutOfStock}
        onClick={() => onAddToCart?.(product.id)}
        className="mt-auto pt-3 w-full py-2 rounded bg-blue-600 text-white disabled:bg-gray-300 disabled:cursor-not-allowed"
        aria-disabled={isOutOfStock}
      >
        Add to Cart
      </button>
    </div>
  )
}
