import { useState, type FormEvent } from 'react'

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>
  sessionExpired?: boolean
}

export function LoginForm({ onSubmit, sessionExpired }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await onSubmit(email, password)
    } catch {
      setError('Incorrect email or password')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {sessionExpired && (
        <p className="text-amber-600 mb-4" role="alert">
          Your session has expired. Please sign in again.
        </p>
      )}

      <div className="mb-4">
        <label htmlFor="login-email" className="block font-medium mb-1">
          Email
        </label>
        <input
          id="login-email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full border rounded px-3 py-2"
          aria-describedby={error ? 'login-error' : undefined}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="login-password" className="block font-medium mb-1">
          Password
        </label>
        <input
          id="login-password"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full border rounded px-3 py-2"
          aria-describedby={error ? 'login-error' : undefined}
        />
      </div>

      {error && (
        <p id="login-error" className="text-red-600 text-sm mb-4" role="alert">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full py-2 bg-blue-600 text-white rounded disabled:bg-gray-300"
      >
        {isSubmitting ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}
