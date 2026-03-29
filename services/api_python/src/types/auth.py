"""
Pydantic schemas for authentication endpoints.
"""

import uuid

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Registration form payload."""

    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)


class RegisterResponse(BaseModel):
    """Successful registration response."""

    id: uuid.UUID
    email: str
    name: str
    message: str = "Account created successfully"
