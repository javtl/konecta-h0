"""
Authentication API endpoints for signup and login.
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import SignupRequest, LoginRequest, TokenResponse
from app.services import auth_service
from app.middleware.auth import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: SignupRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Register a new user account.
    
    **Request body example:**
    ```json
    {
      "email": "user@example.com",
      "username": "johndoe",
      "password": "SecurePassword123!",
      "gym": "Champion Boxing Gym",
      "sport": "BOXING",
      "weight": 75,
      "experience": "INTERMEDIATE"
    }
    ```
    
    **Response example (201 Created):**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "user@example.com"
    }
    ```
    
    **Errors:**
    - 400: Email already registered or username already taken
    - 400: Password must be at least 8 characters
    """
    return await auth_service.signup(db, user_data)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Authenticate user with email and password.
    
    **Request body example:**
    ```json
    {
      "email": "user@example.com",
      "password": "SecurePassword123!"
    }
    ```
    
    **Response example (200 OK):**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "user@example.com"
    }
    ```
    
    **Errors:**
    - 401: Invalid email or password
    """
    return await auth_service.login(db, credentials)
