import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <main className="max-w-md mx-auto px-4 py-16 text-center">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <p className="text-gray-600 mb-6">The page you are looking for does not exist.</p>
      <Link to="/" className="text-blue-600 underline">
        Back to catalogue
      </Link>
    </main>
  )
}
