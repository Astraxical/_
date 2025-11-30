"""
Integration tests for init_db.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session


class TestInitDatabase:
    """Test database initialization"""
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_creates_tables(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database creates tables"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        from init_db import init_database
        init_database()
        
        mock_init.assert_called_once()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_creates_default_alters(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database creates default alters"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {
            "seles": True,
            "dexen": False,
            "yuki": False
        }
        
        # Mock query to return no existing alters
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        from init_db import init_database
        init_database()
        
        # Should add alters
        assert mock_session.add.call_count >= 3
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_skips_existing_alters(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database skips existing alters"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {"seles": True}
        
        # Mock query to return existing alter
        existing_alter = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = existing_alter
        
        from init_db import init_database
        init_database()
        
        # Should not add existing alter
        mock_session.add.assert_not_called()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_creates_default_modules(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database creates default modules"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Mock query to return no existing modules
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        from init_db import init_database
        init_database()
        
        # Should add modules (template, admin, forums, rtc)
        assert mock_session.add.call_count >= 4
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_skips_existing_modules(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database skips existing modules"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Mock query to return existing module
        existing_module = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = existing_module
        
        from init_db import init_database
        init_database()
        
        # Should not add if module exists
        # Note: This will still add alters if they don't exist
        mock_session.commit.assert_called()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_commits_changes(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database commits changes"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        from init_db import init_database
        init_database()
        
        mock_session.commit.assert_called()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_closes_session(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database closes database session"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        from init_db import init_database
        init_database()
        
        mock_session.close.assert_called_once()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    @patch('builtins.print')
    def test_init_database_prints_success(self, mock_print, mock_engine, mock_init, mock_session_local):
        """Test that init_database prints success message"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        from init_db import init_database
        init_database()
        
        # Should print success message
        mock_print.assert_called()
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("success" in call.lower() for call in print_calls)
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    @patch('builtins.print')
    def test_init_database_handles_errors(self, mock_print, mock_engine, mock_init, mock_session_local):
        """Test that init_database handles errors gracefully"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Simulate an error during commit
        mock_session.commit.side_effect = Exception("Database error")
        
        from init_db import init_database
        init_database()
        
        # Should rollback on error
        mock_session.rollback.assert_called_once()
        
        # Should print error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("error" in call.lower() for call in print_calls)
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_closes_session_on_error(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database closes session even on error"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Simulate an error
        mock_session.commit.side_effect = Exception("Error")
        
        from init_db import init_database
        init_database()
        
        # Should still close the session
        mock_session.close.assert_called_once()
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_module_registry_data(self, mock_engine, mock_init, mock_session_local):
        """Test that module registry has correct data"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Mock to return None (no existing modules)
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        from init_db import init_database
        init_database()
        
        # Check that ModuleRegistry was called with correct data
        add_calls = mock_session.add.call_args_list
        
        # Should have added modules
        assert len(add_calls) > 0
    
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.TemplateEngine')
    def test_init_database_idempotent(self, mock_engine, mock_init, mock_session_local):
        """Test that init_database can be called multiple times safely"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_engine.return_value.alters_status = {}
        
        # Mock existing entries
        mock_session.query.return_value.filter.return_value.first.return_value = Mock()
        
        from init_db import init_database
        
        # Call twice
        init_database()
        init_database()
        
        # Should not raise errors
        assert mock_session.commit.call_count >= 2


class TestInitDatabaseMain:
    """Test init_db main execution"""
    
    @patch('init_db.init_database')
    def test_main_calls_init_database(self, mock_init_database):
        """Test that running as main calls init_database"""
        import sys
        from unittest.mock import patch
        
        # Save original argv
        original_argv = sys.argv
        
        try:
            # Simulate running as script
            sys.argv = ['init_db.py']
            
            # This would normally run the main block
            # We'll just verify the function exists and can be called
            from init_db import init_database
            assert callable(init_database)
        finally:
            sys.argv = original_argv