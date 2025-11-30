"""
Comprehensive unit tests for updated init_db.py.
Tests database initialization with alter and module updates.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'codebase'))


class TestInitDatabaseWithAlterUpdates:
    """Test database initialization with alter update logic."""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_updates_existing_alters(self, mock_init, mock_session_local, mock_engine):
        """Test that existing alters are updated instead of recreated."""
        from init_db import init_database
        from utils.db import Alter
        
        # Setup mocks
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {'seles': True, 'dexen': False}
        mock_engine.return_value = mock_template_engine
        
        # Create mock existing alter
        mock_existing_alter = MagicMock(spec=Alter)
        mock_existing_alter.name = 'seles'
        mock_existing_alter.is_fronting = False  # Different from engine status
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_alter
        
        init_database()
        
        # Verify alter was updated
        assert mock_existing_alter.is_fronting == True
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_creates_new_alters_if_not_exist(self, mock_init, mock_session_local, mock_engine):
        """Test that new alters are created if they don't exist."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {'seles': True, 'dexen': False}
        mock_engine.return_value = mock_template_engine
        
        # No existing alter
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Verify new alters were added
        assert mock_db.add.call_count >= 2  # At least 2 alters


class TestInitDatabaseWithModuleUpdates:
    """Test database initialization with module update logic."""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_updates_existing_modules(self, mock_init, mock_session_local, mock_engine):
        """Test that existing modules are updated with new configuration."""
        from init_db import init_database
        from utils.db import ModuleRegistry
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {}
        mock_engine.return_value = mock_template_engine
        
        # Create mock existing module with outdated config
        mock_existing_module = MagicMock(spec=ModuleRegistry)
        mock_existing_module.module_name = 'template'
        mock_existing_module.enabled = False
        mock_existing_module.route_prefix = '/old_template'
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_module
        
        init_database()
        
        # Verify module was updated
        assert mock_existing_module.enabled == True
        assert mock_existing_module.route_prefix == '/template'
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_registers_all_required_modules(self, mock_init, mock_session_local, mock_engine):
        """Test that all required modules are registered."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {}
        mock_engine.return_value = mock_template_engine
        
        # No existing modules
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Should register template, admin, forums, and rtc
        assert mock_db.add.call_count >= 4
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_template_module_registered_first(self, mock_init, mock_session_local, mock_engine):
        """Test that template module is in the list of modules to register."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {}
        mock_engine.return_value = mock_template_engine
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Verify template module was added
        add_calls = [call[0][0] for call in mock_db.add.call_args_list]
        module_names = [getattr(obj, 'module_name', None) for obj in add_calls 
                       if hasattr(obj, 'module_name')]
        
        assert 'template' in module_names


class TestErrorHandling:
    """Test error handling in database initialization."""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_rollback_on_exception(self, mock_init, mock_session_local, mock_engine):
        """Test that database rolls back on exception."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_engine.return_value = mock_template_engine
        
        # Simulate exception during commit
        mock_db.commit.side_effect = Exception("Database error")
        
        init_database()
        
        # Verify rollback was called
        mock_db.rollback.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_closes_session_after_exception(self, mock_init, mock_session_local, mock_engine):
        """Test that database session is closed even after exception."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_engine.return_value = mock_template_engine
        
        mock_db.commit.side_effect = Exception("Database error")
        
        init_database()
        
        # Verify session was closed
        mock_db.close.assert_called_once()


class TestSuccessPath:
    """Test successful database initialization."""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('builtins.print')
    def test_success_message_on_completion(self, mock_print, mock_init, 
                                          mock_session_local, mock_engine):
        """Test that success message is printed on successful initialization."""
        from init_db import init_database
        
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_template_engine = MagicMock()
        mock_template_engine.alters_status = {}
        mock_engine.return_value = mock_template_engine
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        init_database()
        
        # Verify success message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any('successfully' in str(call).lower() for call in print_calls)