import { describe, it, expect, vi } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithProviders, expectNoA11yViolations } from '../helpers/render'
import { ImageGallery } from '../../src/components/ImageGallery'
import { QuantitySelector } from '../../src/components/QuantitySelector'
import { NotFoundPage } from '../../src/components/NotFoundPage'

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
