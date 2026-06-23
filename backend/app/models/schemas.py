"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ==================== Authentication Schemas ====================

class LoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=1, description="User password")


class SignupRequest(BaseModel):
    """User signup request schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    gym: str = Field(..., min_length=1, description="Gym/Team name")
    sport: str = Field(..., description="Sport (BOXING, MMA, MUAY_THAI)")
    weight: int = Field(..., ge=30, le=200, description="Weight in kg")
    experience: str = Field(..., description="Experience level (BEGINNER, INTERMEDIATE, ADVANCED)")


class TokenResponse(BaseModel):
    """Token response schema after login/signup."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    email: str


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: str  # user_id
    exp: int  # timestamp


# ==================== User Schemas ====================

class UserResponse(BaseModel):
    """User response schema for GET endpoints."""
    id: str
    username: str
    email: str
    gym: Optional[str] = None
    sport: str
    weight: int
    experience: str
    total_sparrings: int = 0
    wins: int = 0
    losses: int = 0
    ranking: int = 1000
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
