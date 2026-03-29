import { describe, it, expect, vi } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithProviders, expectNoA11yViolations } from '../helpers/render'
import { ProductCard } from '../../src/components/ProductCard'
import { ProductGrid } from '../../src/components/ProductGrid'
import type { ProductListItem } from '../../src/types/product'

function makeProduct(overrides: Partial<ProductListItem> = {}): ProductListItem {
  return {
    id: 'prod-1',
    name: 'Test Widget',
    price: 29.99,
    thumbnail_url: 'https://example.com/img.jpg',
    stock_quantity: 10,
    stock_status: 'in_stock',
    category_slug: 'electronics',
    ...overrides,
  }
}

describe('ProductCard', () => {
  it('renders product name', () => {
    renderWithProviders(<ProductCard product={makeProduct()} />)
    expect(screen.getByText('Test Widget')).toBeInTheDocument()
  })

  it('renders formatted price', () => {
    renderWithProviders(<ProductCard product={makeProduct({ price: 49.99 })} />)
    expect(screen.getByText('$49.99')).toBeInTheDocument()
  })

  it('renders thumbnail image with alt text', () => {
    renderWithProviders(<ProductCard product={makeProduct()} />)
    const img = screen.getByAltText('Test Widget')
    expect(img).toHaveAttribute('src', 'https://example.com/img.jpg')
  })

  it('shows Out of Stock badge for out of stock products', () => {
    renderWithProviders(
      <ProductCard product={makeProduct({ stock_status: 'out_of_stock' })} />
    )
    expect(screen.getByText('Out of Stock')).toBeInTheDocument()
  })

  it('disables Add to Cart for out of stock products', () => {
    renderWithProviders(
      <ProductCard product={makeProduct({ stock_status: 'out_of_stock' })} />
    )
    const button = screen.getByRole('button', { name: /add to cart/i })
    expect(button).toBeDisabled()
  })

  it('enables Add to Cart for in stock products', () => {
    renderWithProviders(
      <ProductCard product={makeProduct({ stock_status: 'in_stock' })} />
    )
    const button = screen.getByRole('button', { name: /add to cart/i })
    expect(button).toBeEnabled()
  })

  it('calls onAddToCart when clicked', async () => {
    const onAddToCart = vi.fn()
    renderWithProviders(
      <ProductCard product={makeProduct()} onAddToCart={onAddToCart} />
    )
    const user = userEvent.setup()
    await user.click(screen.getByRole('button', { name: /add to cart/i }))
    expect(onAddToCart).toHaveBeenCalledWith('prod-1')
  })

  it('has descriptive aria-label', () => {
    const { container } = renderWithProviders(
      <ProductCard product={makeProduct({ name: 'Widget', price: 19.99 })} />
    )
    const card = container.querySelector('.product-card')
    expect(card).toHaveAttribute('aria-label')
    expect(card?.getAttribute('aria-label')).toContain('Widget')
    expect(card?.getAttribute('aria-label')).toContain('$19.99')
  })

  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(
      <ProductCard product={makeProduct()} />
    )
    await expectNoA11yViolations(container)
  })
})

describe('ProductGrid', () => {
  it('renders multiple products', () => {
    const products = [
      makeProduct({ id: '1', name: 'Widget A' }),
      makeProduct({ id: '2', name: 'Widget B' }),
    ]
    renderWithProviders(<ProductGrid products={products} />)
    expect(screen.getByText('Widget A')).toBeInTheDocument()
    expect(screen.getByText('Widget B')).toBeInTheDocument()
  })

  it('shows empty message when no products', () => {
    renderWithProviders(<ProductGrid products={[]} />)
    expect(screen.getByText(/no products found/i)).toBeInTheDocument()
  })

  it('renders as a list for accessibility', () => {
    const products = [makeProduct()]
    renderWithProviders(<ProductGrid products={products} />)
    expect(screen.getByRole('list')).toBeInTheDocument()
    expect(screen.getAllByRole('listitem')).toHaveLength(1)
  })

  it('has no accessibility violations', async () => {
    const products = [makeProduct()]
    const { container } = renderWithProviders(<ProductGrid products={products} />)
    await expectNoA11yViolations(container)
  })
})
