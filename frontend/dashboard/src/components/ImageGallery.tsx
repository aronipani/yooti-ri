import { useState } from 'react'

interface ImageGalleryProps {
  images: string[]
  productName: string
}

export function ImageGallery({ images, productName }: ImageGalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState(0)

  if (images.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-200 rounded flex items-center justify-center">
        <span className="text-gray-400">No images available</span>
      </div>
    )
  }

  return (
    <div>
      <img
        src={images[selectedIndex]}
        alt={`${productName} - view ${selectedIndex + 1}`}
        className="w-full h-96 object-cover rounded"
      />
      {images.length > 1 && (
        <div className="flex gap-2 mt-2" aria-label="Product thumbnails">
          {images.map((img, i) => (
            <button
              key={img}
              type="button"
              onClick={() => setSelectedIndex(i)}
              className={`w-16 h-16 rounded border-2 ${i === selectedIndex ? 'border-blue-600' : 'border-gray-200'}`}
              aria-label={`View ${productName} ${i + 1}`}
              aria-current={i === selectedIndex ? 'true' : undefined}
            >
              <img src={img} alt={`${productName} ${i + 1}`} className="w-full h-full object-cover rounded" />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
