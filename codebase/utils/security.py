"""
Security utilities for the application
"""
from passlib.context import CryptContext
import secrets
from typing import Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password
    """
    return pwd_context.hash(password)


def generate_secret_key(length: int = 32) -> str:
    """
    Generate a random secret key
    """
    return secrets.token_urlsafe(length)


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Create a JWT access token
    """
    # For now, we'll implement a simple token mechanism
    # In a real application, you'd use python-jose or similar
    import time
    import hashlib
    
    # Create a simple token by hashing the data + timestamp
    to_encode = data.copy()
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + 3600  # 1 hour default
    
    to_encode.update({"exp": expire})
    
    # Create a token by hashing the data
    token_data = str(to_encode)
    token = hashlib.sha256((token_data + generate_secret_key()).encode()).hexdigest()
    
    return token


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify an access token (simplified implementation)
    """
    # In a real application, you'd decode the JWT here
    # This is just a placeholder implementation
    return {"valid": True}