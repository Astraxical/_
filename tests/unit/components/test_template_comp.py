"""
Unit tests for the Template Component
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI

import sys
sys.path.insert(0, 'codebase')

from components.template_comp import setup_template


class TestSetupTemplate:
    """Tests for setup_template function"""
    
    def test_setup_template_includes_router(self):
        """Test that setup_template includes the template router"""
        mock_app = Mock(spec=FastAPI)
        
        with patch('components.template_comp.template_router') as mock_router:
            result = setup_template(mock_app)
            
            # Verify router was included
            mock_app.include_router.assert_called_once_with(mock_router)
    
    def test_setup_template_returns_correct_metadata(self):
        """Test that setup_template returns correct component metadata"""
        mock_app = Mock(spec=FastAPI)
        
        with patch('components.template_comp.template_router'):
            result = setup_template(mock_app)
            
            assert result['name'] == 'template'
            assert '/template/*' in result['routes']
            assert '/template/alter/*' in result['routes']
            assert result['initialized'] is True
    
    def test_setup_template_with_real_fastapi_app(self):
        """Test setup_template with actual FastAPI instance"""
        app = FastAPI()
        
        with patch('components.template_comp.template_router'):
            result = setup_template(app)
            
            assert isinstance(result, dict)
            assert 'name' in result
            assert 'routes' in result
            assert 'initialized' in result
    
    def test_setup_template_routes_list_is_correct_type(self):
        """Test that routes in metadata is a list"""
        mock_app = Mock(spec=FastAPI)
        
        with patch('components.template_comp.template_router'):
            result = setup_template(mock_app)
            
            assert isinstance(result['routes'], list)
            assert len(result['routes']) == 2
    
    def test_setup_template_idempotent(self):
        """Test that setup_template can be called multiple times safely"""
        mock_app = Mock(spec=FastAPI)
        
        with patch('components.template_comp.template_router'):
            result1 = setup_template(mock_app)
            result2 = setup_template(mock_app)
            
            assert result1 == result2
            assert mock_app.include_router.call_count == 2