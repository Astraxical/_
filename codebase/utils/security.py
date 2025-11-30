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
    Check whether a plain password matches a stored hashed password.
    
    Parameters:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The stored password hash to compare against.
    
    Returns:
        bool: `true` if the plaintext password matches the hash, `false` otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using the module's configured password hashing context.
    
    Parameters:
        password (str): Plain-text password to hash.
    
    Returns:
        str: Hashed password suitable for secure storage.
    """
    return pwd_context.hash(password)


def generate_secret_key(length: int = 32) -> str:
    """
    Generate a URL-safe random secret key.
    
    Parameters:
        length (int): Number of random bytes to use before URL-safe base64 encoding (defaults to 32).
    
    Returns:
        str: A URL-safe string encoding the generated random bytes.
    """
    return secrets.token_urlsafe(length)


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Create an opaque access token that encodes the given payload and an expiration timestamp.
    
    Parameters:
        data (dict): Payload to include in the token; will be recorded together with an expiration timestamp.
        expires_delta (Optional[int]): Expiration lifetime in seconds; when omitted, a default of 3600 seconds (1 hour) is used.
    
    Returns:
        token (str): A string token that represents the encoded payload and expiration.
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
    Perform a placeholder verification of an access token.
    
    This implementation does not decode or validate the token and always indicates the token is valid.
    
    Returns:
        dict: A dictionary with key `"valid"` set to `True`.
    """
    # In a real application, you'd decode the JWT here
    # This is just a placeholder implementation
    return {"valid": True}