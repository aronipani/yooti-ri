import { useNavigate } from 'react-router-dom'
import { RegisterForm } from '../components/RegisterForm'
import { useAuth } from '../contexts/AuthContext'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (email: string, password: string, name: string) => {
    await register(email, password, name)
    navigate('/')
  }

  return (
    <main className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold mb-6">Create Account</h1>
      <RegisterForm onSubmit={handleSubmit} />
    </main>
  )
}
