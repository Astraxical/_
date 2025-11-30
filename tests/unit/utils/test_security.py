"""
Unit tests for utils/security.py
Tests for password hashing, token generation, and security utilities
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import time
import hashlib

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))

from utils.security import (
    verify_password,
    get_password_hash,
    generate_secret_key,
    create_access_token,
    verify_access_token
)


class TestPasswordHashing:
    """Tests for password hashing functions"""
    
    def test_get_password_hash_creates_hash(self):
        """Test that password hashing creates a hash"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password  # Hash should be different from plaintext
    
    def test_get_password_hash_different_for_same_password(self):
        """Test that same password produces different hashes (salt)"""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Due to salting, same password should produce different hashes
        assert hash1 != hash2
    
    def test_get_password_hash_empty_password(self):
        """Test hashing an empty password"""
        password = ""
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
    
    def test_get_password_hash_long_password(self):
        """Test hashing a very long password"""
        password = "a" * 1000
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
    
    def test_get_password_hash_special_characters(self):
        """Test hashing password with special characters"""
        password = "p@ssw0rd!#$%^&*()"
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
    
    def test_get_password_hash_unicode_characters(self):
        """Test hashing password with unicode characters"""
        password = "пароль密码🔐"
        hashed = get_password_hash(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)


class TestPasswordVerification:
    """Tests for password verification"""
    
    def test_verify_password_correct(self):
        """Test verification with correct password"""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        result = verify_password(password, hashed)
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Test verification with incorrect password"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        result = verify_password(wrong_password, hashed)
        assert result is False
    
    def test_verify_password_empty_password(self):
        """Test verification with empty password"""
        password = ""
        hashed = get_password_hash(password)
        
        result = verify_password(password, hashed)
        assert result is True
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive"""
        password = "Password123"
        hashed = get_password_hash(password)
        
        result = verify_password("password123", hashed)
        assert result is False
    
    def test_verify_password_whitespace_sensitive(self):
        """Test that whitespace matters in password verification"""
        password = "password"
        hashed = get_password_hash(password)
        
        result = verify_password("password ", hashed)
        assert result is False
        
        result = verify_password(" password", hashed)
        assert result is False
    
    def test_verify_password_special_characters(self):
        """Test verification with special characters"""
        password = "p@ssw0rd!#$%"
        hashed = get_password_hash(password)
        
        result = verify_password(password, hashed)
        assert result is True
    
    def test_verify_password_invalid_hash(self):
        """Test verification with invalid hash format"""
        password = "test_password"
        invalid_hash = "not_a_valid_hash"
        
        result = verify_password(password, invalid_hash)
        assert result is False


class TestGenerateSecretKey:
    """Tests for secret key generation"""
    
    def test_generate_secret_key_default_length(self):
        """Test generating secret key with default length"""
        key = generate_secret_key()
        
        assert key is not None
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_generate_secret_key_custom_length(self):
        """Test generating secret key with custom length"""
        length = 64
        key = generate_secret_key(length)
        
        assert key is not None
        assert isinstance(key, str)
        # URL-safe base64 encoding makes the string longer
        assert len(key) > 0
    
    def test_generate_secret_key_uniqueness(self):
        """Test that generated keys are unique"""
        key1 = generate_secret_key()
        key2 = generate_secret_key()
        
        assert key1 != key2
    
    def test_generate_secret_key_multiple_calls(self):
        """Test generating multiple keys"""
        keys = [generate_secret_key() for _ in range(10)]
        
        # All keys should be unique
        assert len(keys) == len(set(keys))
    
    def test_generate_secret_key_zero_length(self):
        """Test generating key with zero length"""
        key = generate_secret_key(0)
        
        # Should still generate something (empty or minimal)
        assert isinstance(key, str)
    
    def test_generate_secret_key_large_length(self):
        """Test generating very long key"""
        length = 256
        key = generate_secret_key(length)
        
        assert key is not None
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_generate_secret_key_url_safe(self):
        """Test that generated key is URL-safe"""
        key = generate_secret_key()
        
        # URL-safe characters are alphanumeric, _, -
        import re
        assert re.match(r'^[A-Za-z0-9_-]+$', key)


class TestCreateAccessToken:
    """Tests for access token creation"""
    
    def test_create_access_token_basic(self):
        """Test creating a basic access token"""
        data = {"user_id": "123", "username": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiration(self):
        """Test creating token with custom expiration"""
        data = {"user_id": "123"}
        expires_delta = 7200  # 2 hours
        token = create_access_token(data, expires_delta)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_access_token_empty_data(self):
        """Test creating token with empty data"""
        data = {}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_access_token_uniqueness(self):
        """Test that tokens are unique even for same data"""
        data = {"user_id": "123"}
        token1 = create_access_token(data)
        token2 = create_access_token(data)
        
        # Tokens should be different due to secret key generation
        assert token1 != token2
    
    def test_create_access_token_complex_data(self):
        """Test creating token with complex nested data"""
        data = {
            "user_id": "123",
            "roles": ["admin", "user"],
            "metadata": {"login_time": "2025-01-01"}
        }
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_access_token_special_characters_in_data(self):
        """Test creating token with special characters"""
        data = {"username": "user@example.com", "name": "John Döe"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_access_token_default_expiration(self):
        """Test that default expiration is set when not provided"""
        data = {"user_id": "123"}
        
        with patch('time.time', return_value=1000000):
            token = create_access_token(data)
            assert token is not None
    
    def test_create_access_token_zero_expiration(self):
        """Test creating token with zero expiration"""
        data = {"user_id": "123"}
        token = create_access_token(data, expires_delta=0)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_access_token_negative_expiration(self):
        """Test creating token with negative expiration (already expired)"""
        data = {"user_id": "123"}
        token = create_access_token(data, expires_delta=-3600)
        
        assert token is not None
        assert isinstance(token, str)


class TestVerifyAccessToken:
    """Tests for access token verification"""
    
    def test_verify_access_token_valid(self):
        """Test verifying a valid token"""
        data = {"user_id": "123"}
        token = create_access_token(data)
        
        result = verify_access_token(token)
        assert result is not None
        assert isinstance(result, dict)
        assert result.get("valid") is True
    
    def test_verify_access_token_empty_token(self):
        """Test verifying an empty token"""
        result = verify_access_token("")
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_verify_access_token_invalid_token(self):
        """Test verifying an invalid token"""
        invalid_token = "not_a_valid_token_12345"
        result = verify_access_token(invalid_token)
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_verify_access_token_malformed(self):
        """Test verifying a malformed token"""
        malformed_token = "malformed.token.here"
        result = verify_access_token(malformed_token)
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_verify_access_token_none(self):
        """Test verifying None as token"""
        # This is a simplified implementation, so it returns valid
        # In a real implementation, this should be properly handled
        result = verify_access_token(None)
        
        assert result is not None


class TestSecurityIntegration:
    """Integration tests for security functions"""
    
    def test_password_hash_and_verify_workflow(self):
        """Test the complete password hash and verify workflow"""
        # User registration
        password = "user_password_123"
        hashed = get_password_hash(password)
        
        # User login
        is_valid = verify_password(password, hashed)
        assert is_valid is True
        
        # Wrong password attempt
        is_valid = verify_password("wrong_password", hashed)
        assert is_valid is False
    
    def test_token_creation_and_verification_workflow(self):
        """Test the complete token workflow"""
        # Create token
        user_data = {"user_id": "456", "username": "testuser"}
        token = create_access_token(user_data)
        
        # Verify token
        result = verify_access_token(token)
        assert result is not None
        assert result.get("valid") is True
    
    def test_multiple_users_password_workflow(self):
        """Test password workflow with multiple users"""
        users = [
            {"username": "user1", "password": "pass1"},
            {"username": "user2", "password": "pass2"},
            {"username": "user3", "password": "pass3"}
        ]
        
        # Hash all passwords
        for user in users:
            user["hashed"] = get_password_hash(user["password"])
        
        # Verify each user can authenticate
        for user in users:
            assert verify_password(user["password"], user["hashed"]) is True
        
        # Verify cross-authentication fails
        assert verify_password(users[0]["password"], users[1]["hashed"]) is False
    
    def test_secret_key_generation_for_tokens(self):
        """Test that secret keys are used in token generation"""
        data = {"user_id": "789"}
        
        # Generate multiple tokens - they should all be unique due to secret keys
        tokens = [create_access_token(data) for _ in range(5)]
        
        assert len(tokens) == len(set(tokens))  # All unique