from typing import Optional
from fastapi import HTTPException, status
from datetime import timedelta

from core.database import get_database
from core.security import verify_password, get_password_hash, create_access_token
from core.config import settings
from models.user import User
from schemas.user import UserCreate, UserLogin

async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email from database"""
    db = get_database()
    user_dict = await db.users.find_one({"email": email})
    if user_dict:
        user_dict["_id"] = str(user_dict["_id"])
        return User(**user_dict)
    return None

async def create_user(user_data: UserCreate) -> User:
    """Create a new user in the database"""
    db = get_database()
    
    # Check if user already exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user document
    user_dict = {
        "email": user_data.email,
        "hashed_password": hashed_password
    }
    
    # Insert user into database
    result = await db.users.insert_one(user_dict)
    
    # Retrieve the created user
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    
    return User(**created_user)

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    user = await get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

async def login_user(login_data: UserLogin) -> dict:
    """Login user and return access token"""
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

