"""
Unit tests for components/__init__.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI
from components import validate_routes, setup_components


class TestValidateRoutes:
    """Test route validation function"""
    
    def test_validate_routes_no_conflicts(self):
        """Test validation passes with no route conflicts"""
        components = [
            {"name": "admin", "routes": ["/admin/*"]},
            {"name": "forums", "routes": ["/forums/*"]},
            {"name": "rtc", "routes": ["/rtc/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_with_conflict(self):
        """Test validation fails with route conflicts"""
        components = [
            {"name": "module1", "routes": ["/api/*"]},
            {"name": "module2", "routes": ["/api/*"]}
        ]
        
        with pytest.raises(ValueError, match="Route conflict detected: /api/\\*"):
            validate_routes(components)
    
    def test_validate_routes_empty_list(self):
        """Test validation with empty component list"""
        result = validate_routes([])
        assert result is True
    
    def test_validate_routes_no_routes_key(self):
        """Test validation with components without routes key"""
        components = [
            {"name": "module1"},
            {"name": "module2"}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_multiple_routes_per_component(self):
        """Test validation with multiple routes per component"""
        components = [
            {"name": "module1", "routes": ["/api/v1/*", "/api/v2/*"]},
            {"name": "module2", "routes": ["/docs/*", "/help/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_conflict_in_multiple_routes(self):
        """Test conflict detection across multiple routes"""
        components = [
            {"name": "module1", "routes": ["/api/*", "/docs/*"]},
            {"name": "module2", "routes": ["/help/*", "/api/*"]}
        ]
        
        with pytest.raises(ValueError, match="Route conflict detected: /api/\\*"):
            validate_routes(components)
    
    def test_validate_routes_exact_match_required(self):
        """Test that exact route match is required for conflict"""
        components = [
            {"name": "module1", "routes": ["/api/*"]},
            {"name": "module2", "routes": ["/api/v1/*"]}
        ]
        
        # These should not conflict as they're not exact matches
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_case_sensitive(self):
        """Test that route validation is case sensitive"""
        components = [
            {"name": "module1", "routes": ["/API/*"]},
            {"name": "module2", "routes": ["/api/*"]}
        ]
        
        # Different cases should not conflict
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_with_empty_routes(self):
        """Test validation with empty routes list"""
        components = [
            {"name": "module1", "routes": []},
            {"name": "module2", "routes": ["/api/*"]}
        ]
        
        result = validate_routes(components)
        assert result is True
    
    def test_validate_routes_conflict_error_message(self):
        """Test that error message contains the conflicting route"""
        components = [
            {"name": "module1", "routes": ["/test/route/*"]},
            {"name": "module2", "routes": ["/test/route/*"]}
        ]
        
        with pytest.raises(ValueError) as exc_info:
            validate_routes(components)
        
        assert "/test/route/*" in str(exc_info.value)


class TestSetupComponents:
    """Test component setup function"""
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    @patch('components.validate_routes')
    def test_setup_components_calls_all_setup_functions(
        self, mock_validate, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components calls all component setup functions"""
        app = FastAPI()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"], "initialized": True}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"], "initialized": True}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
        mock_validate.return_value = True
        
        setup_components(app)
        
        mock_admin.assert_called_once_with(app)
        mock_forums.assert_called_once_with(app)
        mock_rtc.assert_called_once_with(app)
        mock_validate.assert_called_once()
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    @patch('components.validate_routes')
    def test_setup_components_validates_routes(
        self, mock_validate, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components validates routes"""
        app = FastAPI()
        
        admin_info = {"name": "admin", "routes": ["/admin/*"]}
        forums_info = {"name": "forums", "routes": ["/forums/*"]}
        rtc_info = {"name": "rtc", "routes": ["/rtc/*"]}
        
        mock_admin.return_value = admin_info
        mock_forums.return_value = forums_info
        mock_rtc.return_value = rtc_info
        mock_validate.return_value = True
        
        setup_components(app)
        
        # Check that validate_routes was called with the component info
        call_args = mock_validate.call_args[0][0]
        assert len(call_args) == 3
        assert admin_info in call_args
        assert forums_info in call_args
        assert rtc_info in call_args
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    @patch('components.validate_routes')
    def test_setup_components_raises_on_route_conflict(
        self, mock_validate, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components raises error on route conflict"""
        app = FastAPI()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"]}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"]}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"]}
        mock_validate.side_effect = ValueError("Route conflict detected: /admin/*")
        
        with pytest.raises(ValueError, match="Route conflict detected"):
            setup_components(app)
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    @patch('components.validate_routes')
    @patch('builtins.print')
    def test_setup_components_prints_success_message(
        self, mock_print, mock_validate, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components prints success message"""
        app = FastAPI()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"]}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"]}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"]}
        mock_validate.return_value = True
        
        setup_components(app)
        
        mock_print.assert_called_once()
        print_call = str(mock_print.call_args)
        assert "3" in print_call
        assert "components" in print_call.lower()
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    def test_setup_components_order_of_execution(
        self, mock_rtc, mock_forums, mock_admin
    ):
        """Test that components are set up in correct order"""
        app = FastAPI()
        call_order = []
        
        def admin_setup(app):
            call_order.append('admin')
            return {"name": "admin", "routes": ["/admin/*"]}
        
        def forums_setup(app):
            call_order.append('forums')
            return {"name": "forums", "routes": ["/forums/*"]}
        
        def rtc_setup(app):
            call_order.append('rtc')
            return {"name": "rtc", "routes": ["/rtc/*"]}
        
        mock_admin.side_effect = admin_setup
        mock_forums.side_effect = forums_setup
        mock_rtc.side_effect = rtc_setup
        
        setup_components(app)
        
        # Admin should be first, then forums, then rtc
        assert call_order == ['admin', 'forums', 'rtc']
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    def test_setup_components_with_fastapi_app(
        self, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components receives FastAPI app instance"""
        app = FastAPI()
        
        mock_admin.return_value = {"name": "admin", "routes": ["/admin/*"]}
        mock_forums.return_value = {"name": "forums", "routes": ["/forums/*"]}
        mock_rtc.return_value = {"name": "rtc", "routes": ["/rtc/*"]}
        
        setup_components(app)
        
        # Verify each setup function received the app instance
        assert mock_admin.call_args[0][0] is app
        assert mock_forums.call_args[0][0] is app
        assert mock_rtc.call_args[0][0] is app


class TestComponentIntegration:
    """Test integration between validation and setup"""
    
    def test_components_return_expected_structure(self):
        """Test that component info has expected structure"""
        components = [
            {"name": "test1", "routes": ["/test1/*"], "initialized": True},
            {"name": "test2", "routes": ["/test2/*"], "initialized": True}
        ]
        
        result = validate_routes(components)
        assert result is True
        
        for comp in components:
            assert "name" in comp
            assert "routes" in comp
            assert isinstance(comp["routes"], list)
    
    @patch('components.setup_admin')
    @patch('components.setup_forums')
    @patch('components.setup_rtc')
    def test_setup_components_handles_component_errors(
        self, mock_rtc, mock_forums, mock_admin
    ):
        """Test that setup_components handles component setup errors"""
        app = FastAPI()
        
        mock_admin.side_effect = Exception("Admin setup failed")
        
        with pytest.raises(Exception, match="Admin setup failed"):
            setup_components(app)