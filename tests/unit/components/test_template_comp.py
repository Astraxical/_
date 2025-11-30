"""
Unit tests for template component integration.
Tests the setup and registration of the template module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'codebase'))

from components.template_comp import setup_template


class TestTemplateComponentSetup:
    """Test template component setup and integration."""
    
    def test_setup_template_includes_router(self):
        """Test that setup_template includes the template router."""
        mock_app = MagicMock()
        
        with patch('components.template_comp.template_router') as mock_router:
            result = setup_template(mock_app)
        
        mock_app.include_router.assert_called_once_with(mock_router)
    
    def test_setup_template_returns_correct_metadata(self):
        """Test that setup returns correct component metadata."""
        mock_app = MagicMock()
        
        result = setup_template(mock_app)
        
        assert result['name'] == 'template'
        assert result['initialized'] is True
        assert '/template/*' in result['routes']
        assert '/template/alter/*' in result['routes']
    
    def test_setup_template_with_real_fastapi_app(self):
        """Integration test with actual FastAPI app."""
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_template(app)
        
        assert result['initialized'] is True
        assert len(app.routes) > 0  # Router was mounted


class TestTemplateComponentIntegration:
    """Integration tests for template component."""
    
    @patch('components.template_comp.template_router')
    def test_setup_doesnt_fail_on_multiple_calls(self, mock_router):
        """Test that calling setup multiple times doesn't cause errors."""
        mock_app = MagicMock()
        
        setup_template(mock_app)
        setup_template(mock_app)
        
        # Should be called twice without errors
        assert mock_app.include_router.call_count == 2