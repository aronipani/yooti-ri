/**
 * Test render helper — yooti-ri Frontend
 * Wraps components with providers for testing.
 * Always use renderWithProviders instead of render.
 *
 * Usage:
 *   import { renderWithProviders } from '../helpers/render'
 *   const { getByText } = renderWithProviders(<MyComponent />)
 */
import React, { type ReactElement } from 'react'
import { render, type RenderOptions } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

// Wraps components with all required providers
function AllProviders({ children }: { children: React.ReactNode }) {
  return <MemoryRouter>{children}</MemoryRouter>
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, "wrapper">
) {
  return render(ui, { wrapper: AllProviders, ...options })
}

/**
 * Run axe accessibility check on a container.
 * Call this in EVERY component test.
 *
 * Usage:
 *   const { container } = renderWithProviders(<Button />)
 *   await expectNoA11yViolations(container)
 */
export async function expectNoA11yViolations(container: HTMLElement) {
  const results = await axe(container)
  expect(results).toHaveNoViolations()
}
