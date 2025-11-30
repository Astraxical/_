"""
Unit tests for Template Routes (alter switching)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import APIRouter

import sys
sys.path.insert(0, 'codebase')

from modules.template.routes.alter import switch_alter, get_alter_status, template_engine


class TestSwitchAlterRoute:
    """Tests for switch_alter route handler"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_success(self, mock_engine):
        """Test successful alter switch returns success message"""
        mock_engine.switch_alter.return_value = True
        
        result = switch_alter("dexen")
        
        assert result['success'] is True
        assert "Switched to alter dexen" in result['message']
        mock_engine.switch_alter.assert_called_once_with("dexen")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_failure(self, mock_engine):
        """Test failed alter switch returns failure message"""
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("nonexistent")
        
        assert result['success'] is False
        assert "Failed to switch to alter nonexistent" in result['message']
        mock_engine.switch_alter.assert_called_once_with("nonexistent")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_various_names(self, mock_engine):
        """Test switch_alter with different alter names"""
        mock_engine.switch_alter.return_value = True
        
        test_names = ["seles", "dexen", "yuki", "custom_alter", "test123"]
        
        for name in test_names:
            result = switch_alter(name)
            assert result['success'] is True
            assert name in result['message']
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_special_characters(self, mock_engine):
        """Test switch_alter handles special characters in names"""
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("alter-with-dash")
        
        assert result['success'] is False
        mock_engine.switch_alter.assert_called_once_with("alter-with-dash")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_empty_string(self, mock_engine):
        """Test switch_alter with empty string"""
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("")
        
        assert result['success'] is False
        mock_engine.switch_alter.assert_called_once_with("")


class TestGetAlterStatusRoute:
    """Tests for get_alter_status route handler"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_returns_current_alter(self, mock_engine):
        """Test get_alter_status returns current alter"""
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True, "dexen": False}
        
        result = get_alter_status()
        
        assert result['current_alter'] == "seles"
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_returns_alters_status(self, mock_engine):
        """Test get_alter_status returns all alters status"""
        mock_engine.current_alter = "dexen"
        mock_engine.alters_status = {"seles": False, "dexen": True, "yuki": False}
        
        result = get_alter_status()
        
        assert result['alters_status'] == {"seles": False, "dexen": True, "yuki": False}
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_structure(self, mock_engine):
        """Test get_alter_status returns dict with correct keys"""
        mock_engine.current_alter = "test"
        mock_engine.alters_status = {}
        
        result = get_alter_status()
        
        assert 'current_alter' in result
        assert 'alters_status' in result
        assert isinstance(result, dict)
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_with_multiple_alters(self, mock_engine):
        """Test get_alter_status with multiple alters"""
        mock_engine.current_alter = "alter3"
        mock_engine.alters_status = {
            "alter1": False,
            "alter2": False,
            "alter3": True,
            "alter4": False,
            "alter5": False
        }
        
        result = get_alter_status()
        
        assert result['current_alter'] == "alter3"
        assert len(result['alters_status']) == 5
        assert result['alters_status']['alter3'] is True
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_empty_alters(self, mock_engine):
        """Test get_alter_status with no alters"""
        mock_engine.current_alter = "global"
        mock_engine.alters_status = {}
        
        result = get_alter_status()
        
        assert result['current_alter'] == "global"
        assert result['alters_status'] == {}


class TestRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from modules.template.routes.alter import router
        assert isinstance(router, APIRouter)
    
    def test_template_engine_is_initialized(self):
        """Test that template_engine is initialized"""
        from modules.template.routes.alter import template_engine
        assert template_engine is not None


class TestRouteIntegration:
    """Integration tests for routes"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_and_status_consistency(self, mock_engine):
        """Test that switch_alter and get_alter_status are consistent"""
        # Setup
        mock_engine.switch_alter.return_value = True
        mock_engine.current_alter = "dexen"
        mock_engine.alters_status = {"seles": False, "dexen": True}
        
        # Switch alter
        switch_result = switch_alter("dexen")
        assert switch_result['success'] is True
        
        # Check status
        status_result = get_alter_status()
        assert status_result['current_alter'] == "dexen"
        assert status_result['alters_status']['dexen'] is True