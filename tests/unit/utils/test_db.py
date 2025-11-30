"""
Unit tests for utils/db.py
Tests for database models and initialization
"""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path
from datetime import datetime

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestModuleRegistry:
    """Tests for ModuleRegistry model"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_creation(self, mock_sessionmaker, mock_engine):
        """Test creating a ModuleRegistry instance"""
        from utils.db import ModuleRegistry
        
        module = ModuleRegistry(
            module_name="test_module",
            enabled=True,
            route_prefix="/test",
            local_data_path="modules/test/data"
        )
        
        assert module.module_name == "test_module"
        assert module.enabled is True
        assert module.route_prefix == "/test"
        assert module.local_data_path == "modules/test/data"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_default_enabled(self, mock_sessionmaker, mock_engine):
        """Test that enabled defaults to True"""
        from utils.db import ModuleRegistry
        
        module = ModuleRegistry(
            module_name="test_module",
            route_prefix="/test",
            local_data_path="modules/test/data"
        )
        
        assert module.enabled is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_tablename(self, mock_sessionmaker, mock_engine):
        """Test that table name is correct"""
        from utils.db import ModuleRegistry
        
        assert ModuleRegistry.__tablename__ == "registry"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_disabled_module(self, mock_sessionmaker, mock_engine):
        """Test creating a disabled module"""
        from utils.db import ModuleRegistry
        
        module = ModuleRegistry(
            module_name="disabled_module",
            enabled=False,
            route_prefix="/disabled",
            local_data_path="modules/disabled/data"
        )
        
        assert module.enabled is False
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_timestamps(self, mock_sessionmaker, mock_engine):
        """Test that timestamps are set"""
        from utils.db import ModuleRegistry
        
        module = ModuleRegistry(
            module_name="test_module",
            route_prefix="/test",
            local_data_path="modules/test/data"
        )
        
        # Timestamps should use default values
        assert hasattr(module, 'created_at')
        assert hasattr(module, 'updated_at')


class TestAlter:
    """Tests for Alter model"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_creation(self, mock_sessionmaker, mock_engine):
        """Test creating an Alter instance"""
        from utils.db import Alter
        
        alter = Alter(
            name="seles",
            is_fronting=True,
            bio="Test bio",
            style="purple"
        )
        
        assert alter.name == "seles"
        assert alter.is_fronting is True
        assert alter.bio == "Test bio"
        assert alter.style == "purple"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_default_fronting(self, mock_sessionmaker, mock_engine):
        """Test that is_fronting defaults to False"""
        from utils.db import Alter
        
        alter = Alter(name="dexen")
        
        assert alter.is_fronting is False
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_tablename(self, mock_sessionmaker, mock_engine):
        """Test that table name is correct"""
        from utils.db import Alter
        
        assert Alter.__tablename__ == "alters"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_without_optional_fields(self, mock_sessionmaker, mock_engine):
        """Test creating alter without bio and style"""
        from utils.db import Alter
        
        alter = Alter(name="yuki", is_fronting=False)
        
        assert alter.name == "yuki"
        assert alter.bio is None
        assert alter.style is None
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_timestamps(self, mock_sessionmaker, mock_engine):
        """Test that timestamps are set"""
        from utils.db import Alter
        
        alter = Alter(name="test_alter")
        
        assert hasattr(alter, 'created_at')
        assert hasattr(alter, 'updated_at')
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_multiple_fronting(self, mock_sessionmaker, mock_engine):
        """Test creating multiple alters with different fronting status"""
        from utils.db import Alter
        
        alter1 = Alter(name="alter1", is_fronting=True)
        alter2 = Alter(name="alter2", is_fronting=False)
        alter3 = Alter(name="alter3", is_fronting=False)
        
        assert alter1.is_fronting is True
        assert alter2.is_fronting is False
        assert alter3.is_fronting is False


class TestAuditLog:
    """Tests for AuditLog model"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_creation(self, mock_sessionmaker, mock_engine):
        """Test creating an AuditLog instance"""
        from utils.db import AuditLog
        
        log = AuditLog(
            action="module_enabled",
            user="admin",
            details="Enabled forums module"
        )
        
        assert log.action == "module_enabled"
        assert log.user == "admin"
        assert log.details == "Enabled forums module"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_tablename(self, mock_sessionmaker, mock_engine):
        """Test that table name is correct"""
        from utils.db import AuditLog
        
        assert AuditLog.__tablename__ == "audit_log"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_timestamp(self, mock_sessionmaker, mock_engine):
        """Test that timestamp is set automatically"""
        from utils.db import AuditLog
        
        log = AuditLog(
            action="test_action",
            user="test_user",
            details="test details"
        )
        
        assert hasattr(log, 'timestamp')
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_multiple_entries(self, mock_sessionmaker, mock_engine):
        """Test creating multiple audit log entries"""
        from utils.db import AuditLog
        
        logs = [
            AuditLog(action="login", user="user1", details="User logged in"),
            AuditLog(action="module_toggle", user="admin", details="Toggled forums"),
            AuditLog(action="logout", user="user1", details="User logged out")
        ]
        
        assert len(logs) == 3
        assert all(isinstance(log, AuditLog) for log in logs)
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_empty_details(self, mock_sessionmaker, mock_engine):
        """Test creating audit log with empty details"""
        from utils.db import AuditLog
        
        log = AuditLog(action="test_action", user="test_user", details="")
        
        assert log.details == ""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_long_details(self, mock_sessionmaker, mock_engine):
        """Test creating audit log with long details"""
        from utils.db import AuditLog
        
        long_details = "A" * 1000
        log = AuditLog(action="test_action", user="test_user", details=long_details)
        
        assert log.details == long_details


class TestDatabaseInitialization:
    """Tests for database initialization"""
    
    @patch('utils.db.Base')
    @patch('utils.db.engine')
    def test_init_db_creates_tables(self, mock_engine, mock_base):
        """Test that init_db creates all tables"""
        from utils.db import init_db
        
        mock_metadata = MagicMock()
        mock_base.metadata = mock_metadata
        
        init_db()
        
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)
    
    @patch('utils.db.Base')
    @patch('utils.db.engine')
    def test_init_db_idempotent(self, mock_engine, mock_base):
        """Test that init_db can be called multiple times safely"""
        from utils.db import init_db
        
        mock_metadata = MagicMock()
        mock_base.metadata = mock_metadata
        
        init_db()
        init_db()
        
        # Should be called twice without error
        assert mock_metadata.create_all.call_count == 2


class TestSessionLocal:
    """Tests for database session"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_session_local_created(self, mock_sessionmaker, mock_engine):
        """Test that SessionLocal is created with correct parameters"""
        # Import triggers the creation
        from utils.db import SessionLocal
        
        # Verify sessionmaker was called with correct parameters
        mock_sessionmaker.assert_called_once()
        call_kwargs = mock_sessionmaker.call_args[1]
        assert call_kwargs['autocommit'] is False
        assert call_kwargs['autoflush'] is False


class TestDatabaseEngine:
    """Tests for database engine creation"""
    
    @patch('config.DATABASE_URL', 'sqlite:///test.db')
    @patch('utils.db.create_engine')
    def test_engine_created_with_config_url(self, mock_create_engine):
        """Test that engine is created with URL from config"""
        # Re-import to trigger engine creation with mocked config
        import importlib
        import utils.db
        importlib.reload(utils.db)
        
        # Verify create_engine was called
        assert mock_create_engine.called


class TestModelRelationships:
    """Tests for model relationships and constraints"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_unique_name(self, mock_sessionmaker, mock_engine):
        """Test that module_name has unique constraint"""
        from utils.db import ModuleRegistry
        
        # Check that the column has unique=True
        name_column = ModuleRegistry.__table__.columns.get('module_name')
        assert name_column is not None
        assert name_column.unique is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_unique_name(self, mock_sessionmaker, mock_engine):
        """Test that alter name has unique constraint"""
        from utils.db import Alter
        
        # Check that the column has unique=True
        name_column = Alter.__table__.columns.get('name')
        assert name_column is not None
        assert name_column.unique is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_has_primary_key(self, mock_sessionmaker, mock_engine):
        """Test that ModuleRegistry has primary key"""
        from utils.db import ModuleRegistry
        
        id_column = ModuleRegistry.__table__.columns.get('id')
        assert id_column is not None
        assert id_column.primary_key is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_has_primary_key(self, mock_sessionmaker, mock_engine):
        """Test that Alter has primary key"""
        from utils.db import Alter
        
        id_column = Alter.__table__.columns.get('id')
        assert id_column is not None
        assert id_column.primary_key is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_has_primary_key(self, mock_sessionmaker, mock_engine):
        """Test that AuditLog has primary key"""
        from utils.db import AuditLog
        
        id_column = AuditLog.__table__.columns.get('id')
        assert id_column is not None
        assert id_column.primary_key is True


class TestModelIndexes:
    """Tests for model indexes"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_module_registry_indexed_columns(self, mock_sessionmaker, mock_engine):
        """Test that important columns are indexed"""
        from utils.db import ModuleRegistry
        
        # Check module_name is indexed
        name_column = ModuleRegistry.__table__.columns.get('module_name')
        assert name_column.index is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_alter_indexed_columns(self, mock_sessionmaker, mock_engine):
        """Test that alter name is indexed"""
        from utils.db import Alter
        
        name_column = Alter.__table__.columns.get('name')
        assert name_column.index is True
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_audit_log_indexed_columns(self, mock_sessionmaker, mock_engine):
        """Test that important audit log columns are indexed"""
        from utils.db import AuditLog
        
        # User should be indexed for quick lookups
        user_column = AuditLog.__table__.columns.get('user')
        assert user_column.index is True