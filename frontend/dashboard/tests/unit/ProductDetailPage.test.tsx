import { describe, it, expect, vi, beforeEach } from 'vitest'
import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithProviders, expectNoA11yViolations } from '../helpers/render'
import { ImageGallery } from '../../src/components/ImageGallery'
import { QuantitySelector } from '../../src/components/QuantitySelector'
import { NotFoundPage } from '../../src/components/NotFoundPage'
import { ProductDetailPage } from '../../src/pages/ProductDetailPage'
import { CartDrawer } from '../../src/components/CartDrawer'
import * as cartApi from '../../src/api/cart'
import * as productsApi from '../../src/api/products'
import type { Cart } from '../../src/types/cart'

describe('ImageGallery', () => {
  it('renders main image', () => {
    renderWithProviders(
      <ImageGallery images={['https://example.com/img1.jpg']} productName="Widget" />
    )
    expect(screen.getByAltText(/widget/i)).toBeInTheDocument()
  })

  it('shows thumbnails when multiple images', () => {
    renderWithProviders(
      <ImageGallery
        images={['https://example.com/1.jpg', 'https://example.com/2.jpg']}
        productName="Widget"
      />
    )
    const buttons = screen.getAllByRole('button')
    expect(buttons).toHaveLength(2)
  })

  it('updates main image when thumbnail clicked', async () => {
    renderWithProviders(
      <ImageGallery
        images={['https://example.com/1.jpg', 'https://example.com/2.jpg']}
        productName="Widget"
      />
    )
    const user = userEvent.setup()
    const buttons = screen.getAllByRole('button')
    await user.click(buttons[1])
    const mainImg = screen.getByAltText(/widget - view 2/i)
    expect(mainImg).toHaveAttribute('src', 'https://example.com/2.jpg')
  })

  it('shows placeholder when no images', () => {
    renderWithProviders(<ImageGallery images={[]} productName="Widget" />)
    expect(screen.getByText(/no images available/i)).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(
      <ImageGallery images={['https://example.com/1.jpg']} productName="Widget" />
    )
    await expectNoA11yViolations(container)
  })
})

describe('QuantitySelector', () => {
  it('renders with label', () => {
    renderWithProviders(
      <QuantitySelector value={1} max={10} onChange={vi.fn()} />
    )
    expect(screen.getByLabelText(/quantity/i)).toBeInTheDocument()
  })

  it('caps value at max', () => {
    renderWithProviders(
      <QuantitySelector value={15} max={10} onChange={vi.fn()} />
    )
    expect(screen.getByLabelText(/quantity/i)).toHaveValue(10)
  })

  it('shows warning when value exceeds stock', () => {
    renderWithProviders(
      <QuantitySelector value={15} max={10} onChange={vi.fn()} />
    )
    expect(screen.getByText(/only 10 available/i)).toBeInTheDocument()
  })

  it('has min and max attributes', () => {
    renderWithProviders(
      <QuantitySelector value={1} max={5} onChange={vi.fn()} />
    )
    const input = screen.getByLabelText(/quantity/i)
    expect(input).toHaveAttribute('min', '1')
    expect(input).toHaveAttribute('max', '5')
  })

  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(
      <QuantitySelector value={1} max={10} onChange={vi.fn()} />
    )
    await expectNoA11yViolations(container)
  })
})

describe('NotFoundPage', () => {
  it('shows 404 text', () => {
    renderWithProviders(<NotFoundPage />)
    expect(screen.getByText('404')).toBeInTheDocument()
  })

  it('has a link back to catalogue', () => {
    renderWithProviders(<NotFoundPage />)
    expect(screen.getByRole('link', { name: /back to catalogue/i })).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(<NotFoundPage />)
    await expectNoA11yViolations(container)
  })
})

// ---------------------------------------------------------------------------
// STORY-014 regression tests — Add to Cart wiring in ProductDetailPage
// AC-1: clicking Add to Cart calls cartApi.addToCart with the product id + quantity
// AC-1: cart drawer opens after successful add
// ---------------------------------------------------------------------------

function makeCart(overrides: Partial<Cart> = {}): Cart {
  return {
    items: [],
    subtotal: 0,
    estimated_tax: 0,
    total: 0,
    item_count: 0,
    ...overrides,
  }
}

const mockProduct = {
  id: 'prod-42',
  name: 'Super Widget',
  description: 'A great widget',
  price: 49.99,
  stock_quantity: 5,
  stock_status: 'in_stock' as const,
  thumbnail_url: null,
  images: [],
  category_name: 'Electronics',
  category_slug: 'electronics',
}

describe('ProductDetailPage — Add to Cart wiring (STORY-014)', () => {
  beforeEach(() => {
    vi.spyOn(productsApi, 'getProductById').mockResolvedValue(mockProduct)
    vi.spyOn(cartApi, 'addToCart').mockResolvedValue(
      makeCart({
        items: [{ product_id: 'prod-42', product_name: 'Super Widget', price: 49.99, quantity: 1, subtotal: 49.99, stock_warning: null }],
        item_count: 1,
      })
    )
  })

  it('AC-1: clicking Add to Cart calls cartApi.addToCart with product id and default quantity 1', async () => {
    const user = userEvent.setup()
    renderWithProviders(<><ProductDetailPage /><CartDrawer /></>)

    const button = await screen.findByRole('button', { name: /add to cart/i })
    await user.click(button)

    await waitFor(() => {
      expect(cartApi.addToCart).toHaveBeenCalledWith('prod-42', 1)
    })
  })

  it('AC-1: cart drawer opens after clicking Add to Cart on the detail page', async () => {
    const user = userEvent.setup()
    renderWithProviders(<><ProductDetailPage /><CartDrawer /></>)

    const button = await screen.findByRole('button', { name: /add to cart/i })
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByRole('dialog', { name: /shopping cart/i })).toBeInTheDocument()
    })
  })

  it('AC-1: Add to Cart button is not present when product is out of stock', async () => {
    vi.spyOn(productsApi, 'getProductById').mockResolvedValue({
      ...mockProduct,
      stock_status: 'out_of_stock',
      stock_quantity: 0,
    })

    renderWithProviders(<ProductDetailPage />)

    await screen.findByText(/out of stock/i)
    expect(screen.queryByRole('button', { name: /add to cart/i })).not.toBeInTheDocument()
  })
})
