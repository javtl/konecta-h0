"""
Users API endpoints for retrieving user information.
"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db_models import User
from app.models.schemas import UserResponse
from app.middleware.auth import get_db, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


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
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    ```
    
    **Errors:**
    - 404: User not found
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found"
        )
    
    return user
