import axios from 'axios'
import type { RegisterRequest, RegisterResponse, LoginRequest, LoginResponse } from '../types/auth'

const api = axios.create({ baseURL: '/api/v1/auth' })

export async function register(data: RegisterRequest): Promise<RegisterResponse> {
  const { data: result } = await api.post<RegisterResponse>('/register', data)
  return result
}

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const { data: result } = await api.post<LoginResponse>('/login', data)
  return result
}

export async function logout(): Promise<void> {
  await api.post('/logout')
}
