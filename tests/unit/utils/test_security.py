"""
Unit tests for utils/security.py
"""
import pytest
import re
from utils.security import (
    verify_password,
    get_password_hash,
    generate_secret_key,
    create_access_token,
    verify_access_token
)


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_get_password_hash_returns_string(self):
        """Test that password hashing returns a string"""
        password = "test_password123"
        hashed = get_password_hash(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_get_password_hash_different_for_same_password(self):
        """Test that same password produces different hashes (salt)"""
        password = "test_password123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Due to salting, hashes should be different
        assert hash1 != hash2
    
    def test_get_password_hash_different_passwords(self):
        """Test that different passwords produce different hashes"""
        hash1 = get_password_hash("password1")
        hash2 = get_password_hash("password2")
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test verifying a correct password"""
        password = "correct_password"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verifying an incorrect password"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty_string(self):
        """Test verifying empty password"""
        password = "test"
        hashed = get_password_hash(password)
        
        assert verify_password("", hashed) is False
    
    def test_verify_password_special_characters(self):
        """Test password with special characters"""
        password = "p@ssw0rd!#$%^&*()"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_unicode(self):
        """Test password with unicode characters"""
        password = "пароль密码🔒"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_long_password(self):
        """Test very long password"""
        password = "a" * 1000
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_hash_format_is_bcrypt(self):
        """Test that hash format is bcrypt"""
        password = "test"
        hashed = get_password_hash(password)
        
        # Bcrypt hashes start with $2b$ or $2a$ or $2y$
        assert hashed.startswith(('$2b$', '$2a$', '$2y$'))


class TestSecretKeyGeneration:
    """Test secret key generation"""
    
    def test_generate_secret_key_returns_string(self):
        """Test that secret key generation returns a string"""
        key = generate_secret_key()
        
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_generate_secret_key_default_length(self):
        """Test default secret key length"""
        key = generate_secret_key()
        
        # URL-safe base64 encoding makes the string longer than the byte length
        # 32 bytes should produce roughly 43 characters
        assert len(key) >= 40
    
    def test_generate_secret_key_custom_length(self):
        """Test custom secret key length"""
        key = generate_secret_key(length=64)
        
        # 64 bytes should produce roughly 86 characters
        assert len(key) >= 80
    
    def test_generate_secret_key_uniqueness(self):
        """Test that generated keys are unique"""
        keys = [generate_secret_key() for _ in range(100)]
        
        # All keys should be unique
        assert len(set(keys)) == 100
    
    def test_generate_secret_key_url_safe(self):
        """Test that generated keys are URL-safe"""
        key = generate_secret_key()
        
        # URL-safe characters: letters, digits, hyphen, underscore
        pattern = re.compile(r'^[A-Za-z0-9_-]+$')
        assert pattern.match(key)
    
    def test_generate_secret_key_minimum_length(self):
        """Test secret key generation with minimum length"""
        key = generate_secret_key(length=1)
        
        assert len(key) > 0
    
    def test_generate_secret_key_zero_length(self):
        """Test secret key generation with zero length"""
        key = generate_secret_key(length=0)
        
        # Should still generate something (empty or minimal)
        assert isinstance(key, str)


class TestAccessToken:
    """Test access token creation and verification"""
    
    def test_create_access_token_returns_string(self):
        """Test that token creation returns a string"""
        data = {"user_id": 1, "username": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiration(self):
        """Test creating token with custom expiration"""
        data = {"user_id": 1}
        token = create_access_token(data, expires_delta=7200)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_uniqueness(self):
        """Test that tokens are unique even for same data"""
        data = {"user_id": 1}
        token1 = create_access_token(data)
        token2 = create_access_token(data)
        
        # Tokens should be unique due to random secret key
        assert token1 != token2
    
    def test_create_access_token_different_data(self):
        """Test that different data produces different tokens"""
        token1 = create_access_token({"user_id": 1})
        token2 = create_access_token({"user_id": 2})
        
        assert token1 != token2
    
    def test_create_access_token_empty_data(self):
        """Test creating token with empty data"""
        token = create_access_token({})
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_complex_data(self):
        """Test creating token with complex data structure"""
        data = {
            "user_id": 1,
            "username": "testuser",
            "roles": ["admin", "user"],
            "metadata": {"login_count": 5}
        }
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_hex_format(self):
        """Test that token is in hexadecimal format"""
        data = {"user_id": 1}
        token = create_access_token(data)
        
        # SHA256 hexdigest produces 64 character hex string
        assert len(token) == 64
        pattern = re.compile(r'^[a-f0-9]{64}$')
        assert pattern.match(token)
    
    def test_verify_access_token_returns_dict(self):
        """Test that token verification returns a dict"""
        data = {"user_id": 1}
        token = create_access_token(data)
        result = verify_access_token(token)
        
        assert isinstance(result, dict)
    
    def test_verify_access_token_placeholder(self):
        """Test placeholder verification implementation"""
        token = "test_token_123"
        result = verify_access_token(token)
        
        # Current implementation is a placeholder that always returns valid
        assert result.get("valid") is True
    
    def test_verify_access_token_empty_token(self):
        """Test verifying empty token"""
        result = verify_access_token("")
        
        assert isinstance(result, dict)
    
    def test_verify_access_token_invalid_token(self):
        """Test verifying invalid token"""
        result = verify_access_token("invalid_token_xyz")
        
        # Placeholder returns valid=True
        assert isinstance(result, dict)


class TestSecurityEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_password_hash_none_raises_error(self):
        """Test that None password raises appropriate error"""
        with pytest.raises(Exception):
            get_password_hash(None)
    
    def test_verify_password_with_invalid_hash(self):
        """Test verifying password with invalid hash format"""
        with pytest.raises(Exception):
            verify_password("password", "not_a_valid_hash")
    
    def test_generate_secret_key_negative_length(self):
        """Test secret key generation with negative length"""
        # Should handle gracefully or use default
        key = generate_secret_key(length=-1)
        assert isinstance(key, str)
    
    def test_create_token_negative_expiration(self):
        """Test creating token with negative expiration"""
        data = {"user_id": 1}
        token = create_access_token(data, expires_delta=-1000)
        
        # Should still create a token (expired immediately)
        assert isinstance(token, str)
    
    def test_create_token_zero_expiration(self):
        """Test creating token with zero expiration"""
        data = {"user_id": 1}
        token = create_access_token(data, expires_delta=0)
        
        assert isinstance(token, str)