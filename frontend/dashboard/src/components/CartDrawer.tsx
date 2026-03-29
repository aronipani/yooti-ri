import { useCart } from '../contexts/CartContext'

export function CartDrawer() {
  const { cart, isOpen, closeCart, updateItem, removeItem } = useCart()

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex justify-end" role="dialog" aria-label="Shopping cart">
      <div className="fixed inset-0 bg-black bg-opacity-50" onClick={closeCart} aria-hidden="true" />
      <div className="relative w-96 bg-white h-full shadow-lg flex flex-col">
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-lg font-bold">Your Cart</h2>
          <button type="button" onClick={closeCart} aria-label="Close cart">
            &times;
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4" aria-live="polite">
          {cart.items.length === 0 ? (
            <p className="text-gray-500 text-center">Your cart is empty.</p>
          ) : (
            <ul className="space-y-4">
              {cart.items.map(item => (
                <li key={item.product_id} className="border-b pb-4">
                  <div className="flex justify-between">
                    <span className="font-medium">{item.product_name}</span>
                    <span>${Number(item.subtotal).toFixed(2)}</span>
                  </div>
                  <div className="text-sm text-gray-500">${Number(item.price).toFixed(2)} each</div>
                  <div className="flex items-center gap-2 mt-2">
                    <label htmlFor={`qty-${item.product_id}`} className="sr-only">
                      Quantity for {item.product_name}
                    </label>
                    <input
                      id={`qty-${item.product_id}`}
                      type="number"
                      min={0}
                      value={item.quantity}
                      onChange={e => {
                        const qty = parseInt(e.target.value, 10)
                        if (!isNaN(qty)) void updateItem(item.product_id, qty)
                      }}
                      className="w-16 border rounded px-2 py-1"
                    />
                    <button
                      type="button"
                      onClick={() => void removeItem(item.product_id)}
                      aria-label={`Remove ${item.product_name} from cart`}
                      className="text-red-600 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                  {item.stock_warning && (
                    <p className="text-amber-600 text-sm mt-1" role="alert">
                      {item.stock_warning}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        {cart.items.length > 0 && (
          <div className="p-4 border-t space-y-2">
            <div className="flex justify-between">
              <span>Subtotal</span>
              <span>${Number(cart.subtotal).toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm text-gray-500">
              <span>Estimated Tax</span>
              <span>${Number(cart.estimated_tax).toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-bold text-lg">
              <span>Total</span>
              <span>${Number(cart.total).toFixed(2)}</span>
            </div>
            <button
              type="button"
              className="w-full py-3 bg-blue-600 text-white rounded mt-2"
            >
              Proceed to Checkout
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
