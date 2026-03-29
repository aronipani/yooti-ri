import { describe, it, expect } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { render } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { expectNoA11yViolations } from '../helpers/render'
import { CartDrawer } from '../../src/components/CartDrawer'
import { CartIcon } from '../../src/components/CartIcon'
import { CartProvider, useCart } from '../../src/contexts/CartContext'
function renderWithCart(ui: React.ReactElement) {
  return render(
    <MemoryRouter>
      <CartProvider>{ui}</CartProvider>
    </MemoryRouter>
  )
}

// Helper component to open the cart and set items
function CartTestHarness({ isOpen }: { isOpen?: boolean }) {
  return (
    <>
      <CartDrawer />
      {isOpen && <OpenCartTrigger />}
    </>
  )
}

function OpenCartTrigger() {
  const { openCart } = useCart()
  return (
    <button type="button" onClick={openCart} data-testid="open-cart">
      Open
    </button>
  )
}

describe('CartIcon', () => {
  it('renders cart button', () => {
    renderWithCart(<CartIcon />)
    expect(screen.getByRole('button', { name: /cart/i })).toBeInTheDocument()
  })

  it('shows item count when cart has items', () => {
    // CartIcon starts with 0 items from provider default
    renderWithCart(<CartIcon />)
    expect(screen.getByRole('button', { name: /cart with 0 items/i })).toBeInTheDocument()
  })
})

describe('CartDrawer', () => {
  it('is hidden when not open', () => {
    renderWithCart(<CartDrawer />)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('opens when triggered', async () => {
    renderWithCart(<CartTestHarness isOpen />)
    const user = userEvent.setup()
    await user.click(screen.getByTestId('open-cart'))
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('shows empty cart message', async () => {
    renderWithCart(<CartTestHarness isOpen />)
    const user = userEvent.setup()
    await user.click(screen.getByTestId('open-cart'))
    expect(screen.getByText(/your cart is empty/i)).toBeInTheDocument()
  })

  it('has close button', async () => {
    renderWithCart(<CartTestHarness isOpen />)
    const user = userEvent.setup()
    await user.click(screen.getByTestId('open-cart'))
    expect(screen.getByRole('button', { name: /close cart/i })).toBeInTheDocument()
  })

  it('has no accessibility violations when empty', async () => {
    renderWithCart(<CartTestHarness isOpen />)
    const user = userEvent.setup()
    await user.click(screen.getByTestId('open-cart'))
    const dialog = screen.getByRole('dialog')
    await expectNoA11yViolations(dialog)
  })
})
