import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useProduct } from '../hooks/useProduct'
import { useCart } from '../contexts/CartContext'
import { ImageGallery } from '../components/ImageGallery'
import { QuantitySelector } from '../components/QuantitySelector'
import { NotFoundPage } from '../components/NotFoundPage'

export function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { product, isLoading, isNotFound } = useProduct(id ?? '')
  const { addItem } = useCart()
  const [quantity, setQuantity] = useState(1)

  if (isLoading) return <p className="text-center py-8">Loading...</p>
  if (isNotFound || !product) return <NotFoundPage />

  const isOutOfStock = product.stock_status === 'out_of_stock'

  return (
    <main className="max-w-5xl mx-auto px-4 py-8">
      <Link to="/" className="text-blue-600 underline mb-4 inline-block">
        &larr; Back to catalogue
      </Link>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
        <ImageGallery images={product.images} productName={product.name} />

        <div>
          <p className="text-sm text-gray-500">{product.category_name}</p>
          <h1 className="text-3xl font-bold mt-1">{product.name}</h1>
          <p className="text-2xl font-bold mt-2">${Number(product.price).toFixed(2)}</p>
          <p className="mt-4 text-gray-700">{product.description}</p>

          {isOutOfStock ? (
            <p className="mt-4 text-red-600 font-semibold">Out of Stock</p>
          ) : (
            <div className="mt-4 space-y-4">
              <p className="text-green-600">{product.stock_quantity} in stock</p>
              <QuantitySelector
                value={quantity}
                max={product.stock_quantity}
                onChange={setQuantity}
              />
              <button
                type="button"
                onClick={() => void addItem(product.id, quantity)}
                className="w-full py-3 bg-blue-600 text-white rounded text-lg"
              >
                Add to Cart
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
