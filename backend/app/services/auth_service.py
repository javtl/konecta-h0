"""
Authentication service containing business logic for signup and login.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import timedelta

from app.models.db_models import User
from app.models.schemas import SignupRequest, LoginRequest, TokenResponse
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token
from app.config import get_settings

settings = get_settings()


async def signup(db: AsyncSession, user_data: SignupRequest) -> TokenResponse:
    """
    Register a new user and return an access token.
    
    Args:
        db: AsyncSession database connection
        user_data: SignupRequest with email, username, password, etc.
        
    Returns:
        TokenResponse with access_token, user_id, username, email
        
    Raises:
        HTTPException: If email already exists or username is taken
    """
    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Check if email already exists
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
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
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        gym=user_data.gym,
        sport=user_data.sport,
        weight=user_data.weight,
        experience=user_data.experience
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.id, "email": new_user.email},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        username=new_user.username,
        email=new_user.email
    )


async def login(db: AsyncSession, credentials: LoginRequest) -> TokenResponse:
    """
    Authenticate user with email and password.
    
    Args:
        db: AsyncSession database connection
        credentials: LoginRequest with email and password
        
    Returns:
        TokenResponse with access_token, user_id, username, email
        
    Raises:
        HTTPException: If email not found or password is incorrect
    """
    # Find user by email
    stmt = select(User).where(User.email == credentials.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email
    )
