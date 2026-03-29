import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export function Header() {
  const { user, isAuthenticated, logout } = useAuth()

  return (
    <header className="border-b bg-white">
      <nav className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">
          yooti-ri
        </Link>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <span className="text-sm">{user?.name}</span>
              <button
                type="button"
                onClick={() => void logout()}
                className="text-sm text-red-600 underline"
              >
                Sign Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm underline">
                Sign In
              </Link>
              <Link to="/register" className="text-sm underline">
                Register
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  )
}
