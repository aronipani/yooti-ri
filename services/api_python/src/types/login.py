"""
Pydantic schemas for login/logout endpoints.
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login form payload."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Successful login response."""

    access_token: str
    name: str
    user_id: str
    message: str = "Login successful"
