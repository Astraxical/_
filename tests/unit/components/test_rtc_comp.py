"""
Unit tests for components/rtc_comp.py
Tests for RTC component setup
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestSetupRTC:
    """Tests for setup_rtc function"""
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_includes_router(self, mock_router):
        """Test that setup_rtc includes the rtc router"""
        from components.rtc_comp import setup_rtc
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_rtc(app)
        
        app.include_router.assert_called_once_with(mock_router)
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_returns_info(self, mock_router):
        """Test that setup_rtc returns correct component info"""
        from components.rtc_comp import setup_rtc
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_rtc(app)
        
        assert result is not None
        assert isinstance(result, dict)
        assert result["name"] == "rtc"
        assert result["routes"] == ["/rtc/*"]
        assert result["initialized"] is True
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_with_mock_app(self, mock_router):
        """Test setup_rtc with a mocked FastAPI app"""
        from components.rtc_comp import setup_rtc
        
        mock_app = MagicMock()
        result = setup_rtc(mock_app)
        
        mock_app.include_router.assert_called_once_with(mock_router)
        assert result["initialized"] is True
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_idempotent(self, mock_router):
        """Test that setup_rtc can be called multiple times"""
        from components.rtc_comp import setup_rtc
        
        mock_app = MagicMock()
        
        result1 = setup_rtc(mock_app)
        result2 = setup_rtc(mock_app)
        
        assert result1 == result2
        assert mock_app.include_router.call_count == 2
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_route_prefix(self, mock_router):
        """Test that rtc routes use correct prefix"""
        from components.rtc_comp import setup_rtc
        
        mock_app = MagicMock()
        result = setup_rtc(mock_app)
        
        # Verify the routes list contains rtc prefix
        assert any("/rtc" in route for route in result["routes"])
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_component_name(self, mock_router):
        """Test that component name is correctly set"""
        from components.rtc_comp import setup_rtc
        
        mock_app = MagicMock()
        result = setup_rtc(mock_app)
        
        assert result["name"] == "rtc"
    
    @patch('components.rtc_comp.rtc_router')
    def test_setup_rtc_returns_dict_keys(self, mock_router):
        """Test that returned dict has all required keys"""
        from components.rtc_comp import setup_rtc
        
        mock_app = MagicMock()
        result = setup_rtc(mock_app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result