"""
Tests for utils/security.py
"""
import pytest
import re


def test_password_hashing():
    """Test password hashing functionality"""
    from utils.security import get_password_hash, verify_password
    
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    # Hash should be different from original password
    assert hashed != password
    
    # Hash should be a string
    assert isinstance(hashed, str)
    
    # Hash should have reasonable length (bcrypt produces ~60 char hashes)
    assert len(hashed) > 50


def test_password_verification_success():
    """Test successful password verification"""
    from utils.security import get_password_hash, verify_password
    
    password = "my_secure_password"
    hashed = get_password_hash(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) == True


def test_password_verification_failure():
    """Test failed password verification"""
    from utils.security import get_password_hash, verify_password
    
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed = get_password_hash(password)
    
    # Wrong password should not verify
    assert verify_password(wrong_password, hashed) == False


def test_password_hashing_different_results():
    """Test that same password produces different hashes (due to salt)"""
    from utils.security import get_password_hash
    
    password = "same_password"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different due to salt
    assert hash1 != hash2


def test_password_hashing_empty_string():
    """Test hashing empty string"""
    from utils.security import get_password_hash, verify_password
    
    password = ""
    hashed = get_password_hash(password)
    
    assert isinstance(hashed, str)
    assert verify_password("", hashed) == True
    assert verify_password("not_empty", hashed) == False


def test_password_hashing_special_characters():
    """Test hashing passwords with special characters"""
    from utils.security import get_password_hash, verify_password
    
    password = "p@ssw0rd!#$%^&*()_+"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) == True


def test_password_hashing_unicode():
    """Test hashing passwords with unicode characters"""
    from utils.security import get_password_hash, verify_password
    
    password = "пароль密码🔐"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) == True


def test_generate_secret_key_default_length():
    """Test generating secret key with default length"""
    from utils.security import generate_secret_key
    
    key = generate_secret_key()
    
    assert isinstance(key, str)
    assert len(key) > 0
    # URL-safe base64 encoding produces longer strings than raw bytes
    assert len(key) >= 32


def test_generate_secret_key_custom_length():
    """Test generating secret key with custom length"""
    from utils.security import generate_secret_key
    
    key16 = generate_secret_key(16)
    key64 = generate_secret_key(64)
    
    assert isinstance(key16, str)
    assert isinstance(key64, str)
    assert len(key16) > 0
    assert len(key64) > len(key16)


def test_generate_secret_key_uniqueness():
    """Test that generated keys are unique"""
    from utils.security import generate_secret_key
    
    keys = [generate_secret_key() for _ in range(10)]
    
    # All keys should be unique
    assert len(keys) == len(set(keys))


def test_generate_secret_key_url_safe():
    """Test that generated keys are URL-safe"""
    from utils.security import generate_secret_key
    
    key = generate_secret_key()
    
    # URL-safe base64 uses only alphanumeric, -, and _
    assert re.match(r'^[A-Za-z0-9_-]+$', key)


def test_create_access_token_returns_string():
    """Test that create_access_token returns a string token"""
    from utils.security import create_access_token
    
    data = {"user_id": 123, "username": "testuser"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_with_expiry():
    """Test creating token with custom expiry"""
    from utils.security import create_access_token
    
    data = {"user_id": 456}
    token = create_access_token(data, expires_delta=7200)  # 2 hours
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_different_data_different_tokens():
    """Test that different data produces different tokens"""
    from utils.security import create_access_token
    
    data1 = {"user_id": 1}
    data2 = {"user_id": 2}
    
    token1 = create_access_token(data1)
    token2 = create_access_token(data2)
    
    assert token1 != token2


def test_create_access_token_same_data_different_tokens():
    """Test that same data produces different tokens (due to timestamp/secret)"""
    from utils.security import create_access_token
    import time
    
    data = {"user_id": 123}
    
    token1 = create_access_token(data)
    time.sleep(0.01)  # Small delay
    token2 = create_access_token(data)
    
    # Tokens should be different due to timestamp or random secret
    assert token1 != token2


def test_verify_access_token_returns_dict():
    """Test that verify_access_token returns a dict"""
    from utils.security import verify_access_token, create_access_token
    
    data = {"user_id": 789}
    token = create_access_token(data)
    
    result = verify_access_token(token)
    
    assert isinstance(result, dict)
    assert "valid" in result


def test_verify_access_token_with_invalid_token():
    """Test verifying an invalid token"""
    from utils.security import verify_access_token
    
    # Test with completely invalid token
    result = verify_access_token("invalid_token_12345")
    
    # Should still return a dict (placeholder implementation)
    assert isinstance(result, dict)


def test_password_case_sensitivity():
    """Test that password verification is case-sensitive"""
    from utils.security import get_password_hash, verify_password
    
    password = "Password123"
    hashed = get_password_hash(password)
    
    assert verify_password("Password123", hashed) == True
    assert verify_password("password123", hashed) == False
    assert verify_password("PASSWORD123", hashed) == False


def test_password_hashing_long_password():
    """Test hashing very long passwords"""
    from utils.security import get_password_hash, verify_password
    
    # Create a very long password (1000 characters)
    password = "a" * 1000
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) == True
    assert verify_password("a" * 999, hashed) == False


def test_generate_secret_key_zero_length():
    """Test generating secret key with zero length"""
    from utils.security import generate_secret_key
    
    # Should still generate some key
    key = generate_secret_key(0)
    
    assert isinstance(key, str)


def test_create_access_token_empty_data():
    """Test creating token with empty data"""
    from utils.security import create_access_token
    
    token = create_access_token({})
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_complex_data():
    """Test creating token with complex nested data"""
    from utils.security import create_access_token
    
    data = {
        "user_id": 123,
        "username": "testuser",
        "roles": ["admin", "user"],
        "metadata": {
            "last_login": "2025-01-01",
            "preferences": {"theme": "dark"}
        }
    }
    
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_password_with_wrong_hash_format():
    """Test verification with malformed hash"""
    from utils.security import verify_password
    
    # This should handle gracefully and return False
    result = verify_password("password", "not_a_valid_hash")
    
    assert result == False


def test_password_whitespace_handling():
    """Test that whitespace in passwords is significant"""
    from utils.security import get_password_hash, verify_password
    
    password1 = "password"
    password2 = "password "
    password3 = " password"
    
    hash1 = get_password_hash(password1)
    
    assert verify_password(password1, hash1) == True
    assert verify_password(password2, hash1) == False
    assert verify_password(password3, hash1) == False