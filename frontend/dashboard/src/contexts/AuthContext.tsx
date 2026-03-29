import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'
import type { AuthUser } from '../types/auth'
import * as authApi from '../api/auth'

interface AuthContextValue {
  user: AuthUser | null
  isAuthenticated: boolean
  register: (email: string, password: string, name: string) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)

  const registerFn = useCallback(async (email: string, password: string, name: string) => {
    const result = await authApi.register({ email, password, name })
    setUser({ id: result.id, email: result.email, name: result.name })
  }, [])

  const loginFn = useCallback(async (email: string, password: string) => {
    const result = await authApi.login({ email, password })
    localStorage.setItem('access_token', result.access_token)
    setUser({ id: result.user_id, email, name: result.name })
  }, [])

  const logoutFn = useCallback(async () => {
    await authApi.logout()
    localStorage.removeItem('access_token')
    setUser(null)
  }, [])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: user !== null,
      register: registerFn,
      login: loginFn,
      logout: logoutFn,
    }),
    [user, registerFn, loginFn, logoutFn]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
