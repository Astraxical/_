"""
Unit tests for modules/template/routes/alter.py
Tests for alter switching and status routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent / "codebase"))


class TestSwitchAlterRoute:
    """Tests for switch_alter route"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_success(self, mock_engine):
        """Test successful alter switch"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = True
        
        result = switch_alter("dexen")
        
        assert result["success"] is True
        assert "dexen" in result["message"]
        mock_engine.switch_alter.assert_called_once_with("dexen")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_failure(self, mock_engine):
        """Test failed alter switch"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("nonexistent")
        
        assert result["success"] is False
        assert "Failed" in result["message"]
        assert "nonexistent" in result["message"]
        mock_engine.switch_alter.assert_called_once_with("nonexistent")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_various_names(self, mock_engine):
        """Test switching to various alter names"""
        from modules.template.routes.alter import switch_alter
        
        test_alters = ["seles", "dexen", "yuki", "global"]
        
        for alter_name in test_alters:
            mock_engine.switch_alter.return_value = True
            result = switch_alter(alter_name)
            
            assert result["success"] is True
            assert alter_name in result["message"]
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_special_characters(self, mock_engine):
        """Test switching with special characters in name"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("alter-with-dash")
        
        assert result["success"] is False
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_empty_string(self, mock_engine):
        """Test switching with empty string"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("")
        
        assert result["success"] is False


class TestGetAlterStatusRoute:
    """Tests for get_alter_status route"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_returns_current_alter(self, mock_engine):
        """Test that get_alter_status returns current alter"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True, "dexen": False, "yuki": False}
        
        result = get_alter_status()
        
        assert result["current_alter"] == "seles"
        assert result["alters_status"] == {"seles": True, "dexen": False, "yuki": False}
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_with_global(self, mock_engine):
        """Test status when no alter is fronting (global)"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "global"
        mock_engine.alters_status = {"seles": False, "dexen": False, "yuki": False}
        
        result = get_alter_status()
        
        assert result["current_alter"] == "global"
        assert all(not status for status in result["alters_status"].values())
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_structure(self, mock_engine):
        """Test the structure of the returned status"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "dexen"
        mock_engine.alters_status = {"seles": False, "dexen": True, "yuki": False}
        
        result = get_alter_status()
        
        assert "current_alter" in result
        assert "alters_status" in result
        assert isinstance(result["current_alter"], str)
        assert isinstance(result["alters_status"], dict)
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_with_empty_alters(self, mock_engine):
        """Test status with empty alters dictionary"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "global"
        mock_engine.alters_status = {}
        
        result = get_alter_status()
        
        assert result["current_alter"] == "global"
        assert result["alters_status"] == {}


class TestTemplateRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is properly defined"""
        from modules.template.routes.alter import router
        from fastapi import APIRouter
        
        assert router is not None
        assert isinstance(router, APIRouter)
    
    def test_template_engine_singleton(self):
        """Test that template_engine is a module-level singleton"""
        from modules.template.routes.alter import template_engine
        
        assert template_engine is not None


class TestAlterRoutesEdgeCases:
    """Tests for edge cases in alter routes"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_whitespace(self, mock_engine):
        """Test switching with whitespace in name"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter(" seles ")
        
        # Should fail as it includes whitespace
        assert result["success"] is False
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_case_sensitive(self, mock_engine):
        """Test that alter names are case-sensitive"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("SELES")
        
        # Should pass the exact name to engine
        mock_engine.switch_alter.assert_called_with("SELES")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_concurrent_status_reads(self, mock_engine):
        """Test multiple simultaneous status reads"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "yuki"
        mock_engine.alters_status = {"seles": False, "dexen": False, "yuki": True}
        
        # Simulate concurrent reads
        result1 = get_alter_status()
        result2 = get_alter_status()
        result3 = get_alter_status()
        
        assert result1 == result2 == result3