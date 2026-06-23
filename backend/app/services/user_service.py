"""
User service containing business logic for user creation and retrieval.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import uuid4
from datetime import datetime
import secrets

from app.models.db_models import User
from app.models.schemas import UserCreateRequest
from app.utils.password_utils import hash_password


async def create_user(db: AsyncSession, user_data: UserCreateRequest) -> User:
    """
    Create a new user from admin endpoint.
    
    Args:
        db: AsyncSession database connection
        user_data: UserCreateRequest with email, username, gym, sport, weight, experience
        
    Returns:
        User object (ORM model) with generated random password
        
    Raises:
        HTTPException: If email already exists or username is taken
    """
    # Check if email already exists
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Check if username already exists
    stmt = select(User).where(User.username == user_data.username)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Generate random password (16 chars, secure)
    random_password = secrets.token_urlsafe(16)
    hashed_password = hash_password(random_password)
    
    # Create new user with default octagon stats
    default_octagon = {
        "speed": 5,
        "defense": 5,
        "technique": 5,
        "power": 5,
        "cardio": 5,
        "adaptability": 5,
        "aggression": 5,
        "precision": 5,
    }
    
    now = datetime.utcnow()
    
    new_user = User(
        id=str(uuid4()),
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        gym=user_data.gym,
        sport=user_data.sport,
        weight=user_data.weight,
        experience=user_data.experience,
        octagon=default_octagon,
        ranking=1000,
        total_sparrings=0,
        wins=0,
        losses=0,
        created_at=now,
        updated_at=now
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    """
    Get a user by ID.
    
    Args:
        db: AsyncSession database connection
        user_id: UUID of the user to retrieve
        
    Returns:
        User object (ORM model)
        
    Raises:
        HTTPException: If user not found
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