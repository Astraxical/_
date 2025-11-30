"""
Unit tests for init_db.py
Tests for database initialization script
"""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))


class TestInitDatabase:
    """Tests for init_database function"""
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_calls_init_db(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database calls init_db"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        mock_init_db.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_creates_session(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database creates a database session"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        mock_session_local.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.Alter')
    def test_init_database_creates_alters(self, mock_alter_class, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database creates alters from template engine"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {"seles": True, "dexen": False, "yuki": False}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should create 3 alters
        assert mock_session.add.call_count == 7  # 3 alters + 4 modules
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('init_db.ModuleRegistry')
    def test_init_database_creates_modules(self, mock_module_class, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database creates module registry entries"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should create 4 module entries
        assert mock_session.add.call_count == 4
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_commits_changes(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database commits changes"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        mock_session.commit.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_closes_session(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database closes the session"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        mock_session.close.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('builtins.print')
    def test_init_database_prints_success(self, mock_print, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database prints success message"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Check that success message was printed
        assert any("Database initialized successfully" in str(call) for call in mock_print.call_args_list)
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_skips_existing_alters(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database skips existing alters"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Mock that alter already exists
        existing_alter = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = existing_alter
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {"seles": True}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should not add if already exists
        assert mock_session.add.call_count == 0
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_skips_existing_modules(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database skips existing modules"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Mock that module already exists
        existing_module = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = existing_module
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should not add modules if they already exist
        assert mock_session.add.call_count == 0
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    @patch('builtins.print')
    def test_init_database_handles_exception(self, mock_print, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database handles exceptions"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should rollback on error
        mock_session.rollback.assert_called_once()
        
        # Should print error message
        assert any("Error initializing database" in str(call) for call in mock_print.call_args_list)
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_closes_session_on_error(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that init_database closes session even on error"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.commit.side_effect = Exception("Database error")
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Should close session even after error
        mock_session.close.assert_called_once()
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_module_data(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that module data is correctly structured"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        # Check that modules were added with correct structure
        # Should have called add 4 times for 4 modules
        assert mock_session.add.call_count == 4
    
    @patch('init_db.TemplateEngine')
    @patch('init_db.SessionLocal')
    @patch('init_db.init_db')
    def test_init_database_template_engine_initialization(self, mock_init_db, mock_session_local, mock_template_engine):
        """Test that template engine is initialized"""
        from init_db import init_database
        
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_engine = MagicMock()
        mock_engine.alters_status = {}
        mock_template_engine.return_value = mock_engine
        
        init_database()
        
        mock_template_engine.assert_called_once()