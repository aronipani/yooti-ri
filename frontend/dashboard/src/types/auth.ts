export interface RegisterRequest {
  email: string
  password: string
  name: string
}

export interface RegisterResponse {
  id: string
  email: string
  name: string
  message: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  name: string
  user_id: string
  message: string
}

export interface AuthUser {
  id: string
  email: string
  name: string
}
