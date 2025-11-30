"""
Unit tests for updated init_db.py
Tests for template engine integration and alter/module updates
"""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))


class TestInitDatabaseWithAlters:
    """Tests for init_database function with alter initialization"""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_creates_alters_from_template_engine(self, mock_init, mock_session_class, mock_engine_class):
        """Test that init_database creates alters based on template engine status"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {"seles": True, "dexen": False, "yuki": False}
        mock_engine_class.return_value = mock_engine
        
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Should add all alters from template engine
        assert mock_session.add.call_count >= 3
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_updates_existing_alters(self, mock_init, mock_session_class, mock_engine_class):
        """Test that existing alters are updated"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {"seles": True, "dexen": False}
        mock_engine_class.return_value = mock_engine
        
        # Mock existing alter
        existing_alter = MagicMock()
        existing_alter.name = "seles"
        existing_alter.is_fronting = False
        mock_session.query.return_value.filter.return_value.first.return_value = existing_alter
        
        init_database()
        
        # Should update the existing alter
        assert existing_alter.is_fronting is True
        mock_session.commit.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_adds_template_module(self, mock_init, mock_session_class, mock_engine_class):
        """Test that template module is added to registry"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Check that modules were added (should be at least 4 including template)
        add_calls = mock_session.add.call_args_list
        assert len(add_calls) >= 4
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_updates_existing_modules(self, mock_init, mock_session_class, mock_engine_class):
        """Test that existing modules are updated with new values"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        # Mock existing module
        existing_module = MagicMock()
        existing_module.module_name = "template"
        existing_module.enabled = False
        existing_module.route_prefix = "/old_template"
        mock_session.query.return_value.filter.return_value.first.return_value = existing_module
        
        init_database()
        
        # Should update the existing module
        assert existing_module.enabled is True
        assert existing_module.route_prefix == "/template"
        assert existing_module.local_data_path == "modules/template/data"


class TestInitDatabaseErrorHandling:
    """Tests for error handling in init_database"""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_rolls_back_on_error(self, mock_init, mock_session_class, mock_engine_class):
        """Test that database rollback happens on error"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {"seles": True}
        mock_engine_class.return_value = mock_engine
        
        # Make commit raise an exception
        mock_session.commit.side_effect = Exception("Database error")
        
        init_database()
        
        # Should rollback and close
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('builtins.print')
    def test_init_database_prints_error_message(self, mock_print, mock_init, mock_session_class, mock_engine_class):
        """Test that error message is printed on failure"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        mock_session.commit.side_effect = Exception("Test error")
        
        init_database()
        
        # Should print error message
        error_calls = [call for call in mock_print.call_args_list if "Error" in str(call)]
        assert len(error_calls) > 0
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_always_closes_session(self, mock_init, mock_session_class, mock_engine_class):
        """Test that session is always closed even on error"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        mock_session.add.side_effect = Exception("Add failed")
        
        init_database()
        
        # Session should still be closed
        mock_session.close.assert_called_once()


class TestInitDatabaseModuleRegistry:
    """Tests for module registry initialization"""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_registers_all_four_modules(self, mock_init, mock_session_class, mock_engine_class):
        """Test that all four modules are registered"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Should register template, admin, forums, and rtc
        add_calls = mock_session.add.call_args_list
        # At least 4 modules should be added
        assert len(add_calls) >= 4
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_module_data_structure(self, mock_init, mock_session_class, mock_engine_class):
        """Test that modules have correct data structure"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        captured_modules = []
        
        def capture_add(module):
            if hasattr(module, 'module_name'):
                captured_modules.append(module)
        
        mock_session.add.side_effect = capture_add
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Verify module structure (if any were captured)
        for module in captured_modules:
            assert hasattr(module, 'module_name')
            assert hasattr(module, 'enabled')
            assert hasattr(module, 'route_prefix')
            assert hasattr(module, 'local_data_path')


class TestInitDatabaseSuccess:
    """Tests for successful database initialization"""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('builtins.print')
    def test_init_database_prints_success_message(self, mock_print, mock_init, mock_session_class, mock_engine_class):
        """Test that success message is printed"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Should print success message
        success_calls = [call for call in mock_print.call_args_list if "success" in str(call).lower()]
        assert len(success_calls) > 0
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_calls_init_db(self, mock_init, mock_session_class, mock_engine_class):
        """Test that init_db is called to create tables"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_engine_class.return_value = mock_engine
        
        init_database()
        
        # init_db should be called to create tables
        mock_init.assert_called_once()