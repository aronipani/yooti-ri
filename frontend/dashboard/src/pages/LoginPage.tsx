import { useNavigate, useSearchParams } from 'react-router-dom'
import { LoginForm } from '../components/LoginForm'
import { useAuth } from '../contexts/AuthContext'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const sessionExpired = searchParams.get('expired') === 'true'

  const handleSubmit = async (email: string, password: string) => {
    await login(email, password)
    navigate('/')
  }

  return (
    <main className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold mb-6">Sign In</h1>
      <LoginForm onSubmit={handleSubmit} sessionExpired={sessionExpired} />
    </main>
  )
}
