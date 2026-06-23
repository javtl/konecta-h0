"""
Users API endpoints for retrieving user information and creating users.
"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db_models import User
from app.models.schemas import UserResponse, UserCreateRequest
from app.middleware.auth import get_db, get_current_user
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user (admin endpoint).
    
    **Request body example:**
    ```json
    {
      "email": "boxer2@test.com",
      "username": "juanboxeo2",
      "gym": "Mi Gym",
      "sport": "BOXING",
      "weight": 76,
      "experience": "INTERMEDIATE"
    }
    ```
    
    **Response example (201 Created):**
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "username": "juanboxeo2",
      "email": "boxer2@test.com",
      "gym": "Mi Gym",
      "sport": "BOXING",
      "weight": 76,
      "experience": "INTERMEDIATE",
      "total_sparrings": 0,
      "wins": 0,
      "losses": 0,
      "ranking": 1000,
      "octagon": {
        "speed": 5,
        "defense": 5,
        "technique": 5,
        "power": 5,
        "cardio": 5,
        "adaptability": 5,
        "aggression": 5,
        "precision": 5
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    ```
    
    **Errors:**
    - 400: Email already exists or username is taken
    """
    new_user = await user_service.create_user(db, user_data)
    return new_user


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user's profile.
    
    **Authentication:** Required - Bearer token in Authorization header
    
    **Response example (200 OK):**
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "user@example.com",
      "gym": "Champion Boxing Gym",
      "sport": "BOXING",
      "weight": 75,
      "experience": "INTERMEDIATE",
      "total_sparrings": 0,
      "wins": 0,
      "losses": 0,
      "ranking": 1000,
      "octagon": {
        "speed": 5,
        "defense": 5,
        "technique": 5,
        "power": 5,
        "cardio": 5,
        "adaptability": 5,
        "aggression": 5,
        "precision": 5
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    ```
    
    **Errors:**
    - 401: Invalid or missing authentication token
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get user profile by ID (public endpoint, no authentication required).
    
    **Path Parameters:**
    - user_id: UUID of the user to retrieve
    
    **Response example (200 OK):**
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "user@example.com",
      "gym": "Champion Boxing Gym",
      "sport": "BOXING",
      "weight": 75,
      "experience": "INTERMEDIATE",
      "total_sparrings": 0,
      "wins": 0,
      "losses": 0,
      "ranking": 1000,
      "octagon": {
        "speed": 5,
        "defense": 5,
        "technique": 5,
        "power": 5,
        "cardio": 5,
        "adaptability": 5,
        "aggression": 5,
        "precision": 5
      },
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    ```
    
    **Errors:**
    - 404: User not found
    """
    user = await user_service.get_user_by_id(db, user_id)
    return user
