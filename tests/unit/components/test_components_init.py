"""
Unit tests for components/__init__.py
Tests for component setup and route validation
"""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))

from components import validate_routes, setup_components


class TestValidateRoutes:
    """Tests for validate_routes function"""
    
    def test_validate_routes_no_conflicts(self):
        """Test validation passes when no route conflicts exist"""
        components = [
            {"name": "admin", "routes": ["/admin/*"]},
            {"name": "forums", "routes": ["/forums/*"]},
            {"name": "rtc", "routes": ["/rtc/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_with_conflict(self):
        """Test validation fails when route conflicts exist"""
        components = [
            {"name": "admin", "routes": ["/admin/*"]},
            {"name": "forums", "routes": ["/admin/*"]},  # Conflict!
        ]
        
        with pytest.raises(ValueError, match="Route conflict detected: /admin/\\*"):
            validate_routes(components)
    
    def test_validate_routes_empty_list(self):
        """Test validation with empty components list"""
        components = []
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_no_routes_key(self):
        """Test validation when component has no routes key"""
        components = [
            {"name": "admin"},  # No routes key
            {"name": "forums", "routes": ["/forums/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_empty_routes(self):
        """Test validation with empty routes list"""
        components = [
            {"name": "admin", "routes": []},
            {"name": "forums", "routes": ["/forums/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_multiple_routes_per_component(self):
        """Test validation with multiple routes per component"""
        components = [
            {"name": "admin", "routes": ["/admin/*", "/admin/dashboard/*"]},
            {"name": "forums", "routes": ["/forums/*", "/forums/threads/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_conflict_in_multiple_routes(self):
        """Test detection of conflict in multiple routes"""
        components = [
            {"name": "admin", "routes": ["/admin/*", "/shared/*"]},
            {"name": "forums", "routes": ["/forums/*", "/shared/*"]}  # Conflict!
        ]
        
        with pytest.raises(ValueError, match="Route conflict detected: /shared/\\*"):
            validate_routes(components)
    
    def test_validate_routes_exact_match_required(self):
        """Test that only exact matches are considered conflicts"""
        components = [
            {"name": "admin", "routes": ["/admin/*"]},
            {"name": "forums", "routes": ["/admin/forums/*"]}  # Not a conflict
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_case_sensitive(self):
        """Test that route validation is case-sensitive"""
        components = [
            {"name": "admin", "routes": ["/Admin/*"]},
            {"name": "forums", "routes": ["/admin/*"]}  # Different case
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_special_characters(self):
        """Test validation with special characters in routes"""
        components = [
            {"name": "api", "routes": ["/api/v1/*"]},
            {"name": "api_v2", "routes": ["/api/v2/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True


class TestSetupComponents:
    """Tests for setup_components function"""
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    def test_setup_components_all_modules(self, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test setting up all components"""
        mock_app = MagicMock()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(mock_app)
        
        # Verify all setup functions were called
        mock_admin.assert_called_once_with(mock_app)
        mock_forums.assert_called_once_with(mock_app)
        mock_rtc.assert_called_once_with(mock_app)
        
        # Verify validation was called
        mock_validate.assert_called_once()
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    def test_setup_components_validates_routes(self, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test that setup validates routes"""
        mock_app = MagicMock()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(mock_app)
        
        # Check that validate_routes was called with component info
        call_args = mock_validate.call_args[0][0]
        assert len(call_args) == 3
        assert all("name" in comp for comp in call_args)
        assert all("routes" in comp for comp in call_args)
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    def test_setup_components_order(self, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test that components are set up in correct order"""
        mock_app = MagicMock()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(mock_app)
        
        # Verify order: admin, forums, rtc
        assert mock_admin.call_args < mock_forums.call_args
        assert mock_forums.call_args < mock_rtc.call_args
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    @patch('builtins.print')
    def test_setup_components_prints_success(self, mock_print, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test that setup prints success message"""
        mock_app = MagicMock()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(mock_app)
        
        # Check that success message was printed
        mock_print.assert_called_once()
        assert "Successfully set up 3 components" in str(mock_print.call_args)
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    def test_setup_components_validation_failure(self, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test that validation failure raises error"""
        mock_app = MagicMock()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/admin/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.side_effect = ValueError("Route conflict detected: /admin/*")
        
        with pytest.raises(ValueError, match="Route conflict detected"):
            setup_components(mock_app)
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    @patch('components.validate_routes')
    def test_setup_components_with_fastapi_app(self, mock_validate, mock_admin, mock_forums, mock_rtc):
        """Test setup with actual FastAPI app structure"""
        from fastapi import FastAPI
        app = FastAPI()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(app)
        
        # Verify all components were set up with the app
        mock_admin.assert_called_once_with(app)
        mock_forums.assert_called_once_with(app)
        mock_rtc.assert_called_once_with(app)


class TestComponentIntegration:
    """Integration tests for component setup"""
    
    @patch('components.setup_rtc')
    @patch('components.setup_forums')
    @patch('components.setup_admin')
    def test_component_info_structure(self, mock_admin, mock_forums, mock_rtc):
        """Test that component info has correct structure"""
        mock_app = MagicMock()
        
        admin_info = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        forums_info = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        rtc_info = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        
        mock_admin.return_value = admin_info
        mock_forums.return_value = forums_info
        mock_rtc.return_value = rtc_info
        
        setup_components(mock_app)
        
        # All components should return dicts with required keys
        for info in [admin_info, forums_info, rtc_info]:
            assert "name" in info
            assert "routes" in info
            assert "initialized" in info
            assert info["initialized"] is True
    
    def test_validate_routes_performance(self):
        """Test validation performance with many components"""
        # Create 100 components with unique routes
        components = [
            {"name": f"module_{i}", "routes": [f"/module_{i}/*"]}
            for i in range(100)
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_deep_paths(self):
        """Test validation with deeply nested route paths"""
        components = [
            {"name": "api", "routes": ["/api/v1/users/profile/settings/*"]},
            {"name": "admin", "routes": ["/admin/dashboard/modules/config/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True