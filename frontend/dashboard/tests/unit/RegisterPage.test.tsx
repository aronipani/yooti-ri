import { describe, it, expect, vi } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { renderWithProviders, expectNoA11yViolations } from '../helpers/render'
import { RegisterForm } from '../../src/components/RegisterForm'

const mockSubmit = vi.fn().mockResolvedValue(undefined)

describe('RegisterForm', () => {
  it('renders all form fields', () => {
    renderWithProviders(<RegisterForm onSubmit={mockSubmit} />)
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('shows error for invalid email format', async () => {
    renderWithProviders(<RegisterForm onSubmit={mockSubmit} />)
    const user = userEvent.setup()
    await user.type(screen.getByLabelText(/name/i), 'Test')
    await user.type(screen.getByLabelText(/email/i), 'not-an-email')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /create account/i }))
    expect(screen.getByText(/please enter a valid email/i)).toBeInTheDocument()
  })

  it('shows error for short password', async () => {
    renderWithProviders(<RegisterForm onSubmit={mockSubmit} />)
    const user = userEvent.setup()
    await user.type(screen.getByLabelText(/name/i), 'Test')
    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'short')
    await user.click(screen.getByRole('button', { name: /create account/i }))
    expect(screen.getByText(/at least 8 characters/i)).toBeInTheDocument()
  })

  it('does not call onSubmit when validation fails', async () => {
    const submit = vi.fn()
    renderWithProviders(<RegisterForm onSubmit={submit} />)
    const user = userEvent.setup()
    await user.click(screen.getByRole('button', { name: /create account/i }))
    expect(submit).not.toHaveBeenCalled()
  })

  it('calls onSubmit with valid data', async () => {
    const submit = vi.fn().mockResolvedValue(undefined)
    renderWithProviders(<RegisterForm onSubmit={submit} />)
    const user = userEvent.setup()
    await user.type(screen.getByLabelText(/name/i), 'Test User')
    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /create account/i }))
    expect(submit).toHaveBeenCalledWith('test@example.com', 'password123', 'Test User')
  })

  it('preserves form data on server error', async () => {
    const submit = vi.fn().mockRejectedValue({
      response: { data: { detail: 'An account with this email already exists' } },
    })
    renderWithProviders(<RegisterForm onSubmit={submit} />)
    const user = userEvent.setup()
    await user.type(screen.getByLabelText(/name/i), 'Test')
    await user.type(screen.getByLabelText(/email/i), 'taken@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /create account/i }))

    expect(screen.getByText(/already exists/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toHaveValue('taken@example.com')
  })

  it('has no accessibility violations', async () => {
    const { container } = renderWithProviders(<RegisterForm onSubmit={mockSubmit} />)
    await expectNoA11yViolations(container)
  })
})
