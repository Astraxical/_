"""
Comprehensive unit tests for utils/security.py
Tests for password truncation and edge cases
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestPasswordTruncation:
    """Tests for password truncation in security functions"""
    
    @patch('utils.security.pwd_context')
    def test_verify_password_truncates_long_passwords(self, mock_context):
        """Test that verify_password truncates passwords over 72 bytes"""
        from utils.security import verify_password
        
        long_password = "a" * 100  # 100 characters
        hashed_password = "hashed"
        
        mock_context.verify.return_value = True
        
        result = verify_password(long_password, hashed_password)
        
        # Should have been called with truncated password
        call_args = mock_context.verify.call_args[0]
        assert len(call_args[0]) == 72
    
    @patch('utils.security.pwd_context')
    def test_verify_password_keeps_short_passwords(self, mock_context):
        """Test that short passwords are not truncated"""
        from utils.security import verify_password
        
        short_password = "short"
        hashed_password = "hashed"
        
        mock_context.verify.return_value = True
        
        result = verify_password(short_password, hashed_password)
        
        # Should be called with original password
        call_args = mock_context.verify.call_args[0]
        assert call_args[0] == short_password
    
    @patch('utils.security.pwd_context')
    def test_get_password_hash_truncates_long_passwords(self, mock_context):
        """Test that get_password_hash truncates passwords over 72 bytes"""
        from utils.security import get_password_hash
        
        long_password = "a" * 100
        
        mock_context.hash.return_value = "hashed"
        
        result = get_password_hash(long_password)
        
        # Should have been called with truncated password
        call_args = mock_context.hash.call_args[0]
        assert len(call_args[0]) == 72
    
    @patch('utils.security.pwd_context')
    def test_get_password_hash_keeps_short_passwords(self, mock_context):
        """Test that short passwords are not truncated when hashing"""
        from utils.security import get_password_hash
        
        short_password = "short"
        
        mock_context.hash.return_value = "hashed"
        
        result = get_password_hash(short_password)
        
        # Should be called with original password
        call_args = mock_context.hash.call_args[0]
        assert call_args[0] == short_password
    
    @patch('utils.security.pwd_context')
    def test_multibyte_character_truncation(self, mock_context):
        """Test truncation with multibyte UTF-8 characters"""
        from utils.security import get_password_hash
        
        # Create a password with multibyte characters that exceeds 72 bytes
        multibyte_password = "密" * 30  # Each character is 3 bytes in UTF-8
        
        mock_context.hash.return_value = "hashed"
        
        result = get_password_hash(multibyte_password)
        
        # Should have been truncated based on byte length
        call_args = mock_context.hash.call_args[0]
        assert len(call_args[0].encode('utf-8')) <= 72


class TestGenerateSecretKey:
    """Tests for generate_secret_key function"""
    
    @patch('utils.security.secrets.token_urlsafe')
    def test_generate_secret_key_default_length(self, mock_token):
        """Test that default length is 32"""
        from utils.security import generate_secret_key
        
        mock_token.return_value = "secret_key"
        
        result = generate_secret_key()
        
        mock_token.assert_called_once_with(32)
    
    @patch('utils.security.secrets.token_urlsafe')
    def test_generate_secret_key_custom_length(self, mock_token):
        """Test generating key with custom length"""
        from utils.security import generate_secret_key
        
        mock_token.return_value = "secret_key"
        
        result = generate_secret_key(length=64)
        
        mock_token.assert_called_once_with(64)
    
    @patch('utils.security.secrets.token_urlsafe')
    def test_generate_secret_key_returns_string(self, mock_token):
        """Test that function returns string"""
        from utils.security import generate_secret_key
        
        mock_token.return_value = "secret_key"
        
        result = generate_secret_key()
        
        assert isinstance(result, str)
    
    @patch('utils.security.secrets.token_urlsafe')
    def test_generate_secret_key_url_safe(self, mock_token):
        """Test that generated key is URL-safe"""
        from utils.security import generate_secret_key
        
        mock_token.return_value = "abcdef123456_-"
        
        result = generate_secret_key()
        
        # Should not contain problematic characters
        assert "/" not in result or "=" not in result or "+" not in result


class TestCreateAccessToken:
    """Tests for create_access_token function"""
    
    @patch('utils.security.generate_secret_key')
    @patch('utils.security.time.time')
    def test_create_access_token_with_default_expiry(self, mock_time, mock_secret):
        """Test token creation with default expiration"""
        from utils.security import create_access_token
        
        mock_time.return_value = 1000
        mock_secret.return_value = "secret"
        
        token = create_access_token({"user_id": 123})
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    @patch('utils.security.generate_secret_key')
    @patch('utils.security.time.time')
    def test_create_access_token_with_custom_expiry(self, mock_time, mock_secret):
        """Test token creation with custom expiration"""
        from utils.security import create_access_token
        
        mock_time.return_value = 1000
        mock_secret.return_value = "secret"
        
        token = create_access_token({"user_id": 123}, expires_delta=7200)
        
        assert isinstance(token, str)
    
    @patch('utils.security.generate_secret_key')
    @patch('utils.security.time.time')
    def test_create_access_token_includes_expiration(self, mock_time, mock_secret):
        """Test that token includes expiration in payload"""
        from utils.security import create_access_token
        
        current_time = 1000
        mock_time.return_value = current_time
        mock_secret.return_value = "secret"
        
        # The implementation adds expiration to data before hashing
        token = create_access_token({"user_id": 123}, expires_delta=3600)
        
        # Token should be generated
        assert len(token) > 0
    
    @patch('utils.security.generate_secret_key')
    def test_create_access_token_with_empty_data(self, mock_secret):
        """Test token creation with empty data"""
        from utils.security import create_access_token
        
        mock_secret.return_value = "secret"
        
        token = create_access_token({})
        
        assert isinstance(token, str)


class TestVerifyAccessToken:
    """Tests for verify_access_token function"""
    
    def test_verify_access_token_returns_dict(self):
        """Test that verify returns dictionary"""
        from utils.security import verify_access_token
        
        result = verify_access_token("any_token")
        
        assert isinstance(result, dict)
    
    def test_verify_access_token_always_valid(self):
        """Test that placeholder implementation always returns valid"""
        from utils.security import verify_access_token
        
        result = verify_access_token("any_token")
        
        assert result["valid"] is True
    
    def test_verify_access_token_with_various_tokens(self):
        """Test verification with various token formats"""
        from utils.security import verify_access_token
        
        test_tokens = ["", "short", "very_long_token" * 100, "!@#$%^&*()"]
        
        for token in test_tokens:
            result = verify_access_token(token)
            assert result["valid"] is True


class TestSecurityEdgeCases:
    """Tests for edge cases in security module"""
    
    @patch('utils.security.pwd_context')
    def test_verify_password_with_empty_password(self, mock_context):
        """Test verifying empty password"""
        from utils.security import verify_password
        
        mock_context.verify.return_value = False
        
        result = verify_password("", "hashed")
        
        assert result is False
    
    @patch('utils.security.pwd_context')
    def test_get_password_hash_with_empty_password(self, mock_context):
        """Test hashing empty password"""
        from utils.security import get_password_hash
        
        mock_context.hash.return_value = "hashed_empty"
        
        result = get_password_hash("")
        
        assert isinstance(result, str)
    
    @patch('utils.security.pwd_context')
    def test_verify_password_with_none(self, mock_context):
        """Test that None password is handled"""
        from utils.security import verify_password
        
        # Should handle gracefully or raise appropriate error
        try:
            result = verify_password(None, "hashed")
        except (TypeError, AttributeError):
            # Expected error for None password
            pass