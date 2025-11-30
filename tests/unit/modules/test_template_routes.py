"""
Unit tests for template module routes (alter switching).
Tests API endpoints for alter management.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'codebase'))


class TestAlterSwitchEndpoint:
    """Test the alter switch API endpoint."""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_success(self, mock_engine):
        """Test successful alter switch returns success message."""
        from modules.template.routes.alter import router
        from fastapi import FastAPI
        
        mock_engine.switch_alter.return_value = True
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get('/switch/dexen')
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'dexen' in response.json()['message']
        mock_engine.switch_alter.assert_called_once_with('dexen')
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_failure(self, mock_engine):
        """Test failed alter switch returns error message."""
        from modules.template.routes.alter import router
        from fastapi import FastAPI
        
        mock_engine.switch_alter.return_value = False
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get('/switch/invalid')
        
        assert response.status_code == 200
        assert response.json()['success'] is False
        assert 'Failed' in response.json()['message']
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_special_characters(self, mock_engine):
        """Test alter switch with special characters in name."""
        from modules.template.routes.alter import router
        from fastapi import FastAPI
        
        mock_engine.switch_alter.return_value = False
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get('/switch/test-alter_123')
        
        assert response.status_code == 200
        mock_engine.switch_alter.assert_called_once_with('test-alter_123')


class TestAlterStatusEndpoint:
    """Test the alter status API endpoint."""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status(self, mock_engine):
        """Test retrieving current alter status."""
        from modules.template.routes.alter import router
        from fastapi import FastAPI
        
        mock_engine.current_alter = 'seles'
        mock_engine.alters_status = {'seles': True, 'dexen': False, 'yuki': False}
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get('/status')
        
        assert response.status_code == 200
        data = response.json()
        assert data['current_alter'] == 'seles'
        assert data['alters_status'] == {'seles': True, 'dexen': False, 'yuki': False}
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_no_fronting(self, mock_engine):
        """Test status when no alter is fronting."""
        from modules.template.routes.alter import router
        from fastapi import FastAPI
        
        mock_engine.current_alter = 'global'
        mock_engine.alters_status = {}
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get('/status')
        
        assert response.status_code == 200
        assert response.json()['current_alter'] == 'global'
        assert response.json()['alters_status'] == {}


class TestRouterConfiguration:
    """Test router configuration and setup."""
    
    def test_router_exists(self):
        """Test that the router is properly configured."""
        from modules.template.routes.alter import router
        
        assert router is not None
        assert len(router.routes) >= 2  # At least switch and status endpoints
    
    def test_template_engine_singleton(self):
        """Test that template_engine is created as module-level singleton."""
        from modules.template.routes.alter import template_engine
        
        assert template_engine is not None
        assert hasattr(template_engine, 'switch_alter')
        assert hasattr(template_engine, 'current_alter')
        assert hasattr(template_engine, 'alters_status')