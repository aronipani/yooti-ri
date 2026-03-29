interface QuantitySelectorProps {
  value: number
  max: number
  onChange: (quantity: number) => void
}

export function QuantitySelector({ value, max, onChange }: QuantitySelectorProps) {
  const capped = Math.min(value, max)

  return (
    <div>
      <label htmlFor="quantity" className="block font-medium mb-1">
        Quantity
      </label>
      <input
        id="quantity"
        type="number"
        min={1}
        max={max}
        value={capped}
        onChange={e => {
          const num = parseInt(e.target.value, 10)
          if (!isNaN(num)) onChange(Math.min(num, max))
        }}
        className="w-20 border rounded px-2 py-1"
        aria-describedby={value > max ? 'qty-warning' : undefined}
      />
      {value > max && (
        <p id="qty-warning" className="text-amber-600 text-sm mt-1" role="alert">
          Only {max} available. Quantity adjusted.
        </p>
      )}
    </div>
  )
}
