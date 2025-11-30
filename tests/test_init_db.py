"""
Tests for init_db.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


def test_init_database_creates_tables(test_db_session, monkeypatch):
    """Test that init_database creates database tables"""
    from utils.db import Base, engine
    
    # Mock the SessionLocal to return our test session
    mock_session_local = Mock(return_value=test_db_session)
    
    # Mock TemplateEngine to avoid file dependencies
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {
        "seles": True,
        "dexen": False,
        "yuki": False
    }
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            # Should not raise an exception
            init_database()


def test_init_database_creates_default_alters(test_db_session):
    """Test that init_database creates default alters"""
    from utils.db import Alter
    
    mock_session_local = Mock(return_value=test_db_session)
    
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {
        "alter1": True,
        "alter2": False
    }
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            alters = test_db_session.query(Alter).all()
            assert len(alters) == 2
            
            alter_names = [a.name for a in alters]
            assert "alter1" in alter_names
            assert "alter2" in alter_names


def test_init_database_creates_module_registry(test_db_session):
    """Test that init_database creates module registry entries"""
    from utils.db import ModuleRegistry
    
    mock_session_local = Mock(return_value=test_db_session)
    
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            modules = test_db_session.query(ModuleRegistry).all()
            assert len(modules) == 4
            
            module_names = [m.module_name for m in modules]
            assert "template" in module_names
            assert "admin" in module_names
            assert "forums" in module_names
            assert "rtc" in module_names


def test_init_database_module_registry_details(test_db_session):
    """Test that module registry has correct details"""
    from utils.db import ModuleRegistry
    
    mock_session_local = Mock(return_value=test_db_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            admin_module = test_db_session.query(ModuleRegistry).filter_by(module_name="admin").first()
            
            assert admin_module is not None
            assert admin_module.enabled == True
            assert admin_module.route_prefix == "/admin"
            assert admin_module.local_data_path == "modules/admin/data"


def test_init_database_idempotent(test_db_session):
    """Test that init_database can be called multiple times safely"""
    from utils.db import ModuleRegistry, Alter
    
    mock_session_local = Mock(return_value=test_db_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {"test_alter": True}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            # Call twice
            init_database()
            init_database()
            
            # Should only have one of each
            alters = test_db_session.query(Alter).filter_by(name="test_alter").all()
            assert len(alters) == 1
            
            modules = test_db_session.query(ModuleRegistry).filter_by(module_name="admin").all()
            assert len(modules) == 1


def test_init_database_handles_errors(test_db_session):
    """Test that init_database handles errors gracefully"""
    mock_session = Mock()
    mock_session.query.side_effect = Exception("Database error")
    mock_session.rollback = Mock()
    mock_session.close = Mock()
    
    mock_session_local = Mock(return_value=mock_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            # Should not raise exception
            init_database()
            
            # Should call rollback and close
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()


def test_init_database_sets_alter_fronting_status(test_db_session):
    """Test that alters are created with correct fronting status"""
    from utils.db import Alter
    
    mock_session_local = Mock(return_value=test_db_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {
        "fronting_alter": True,
        "not_fronting_alter": False
    }
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            fronting = test_db_session.query(Alter).filter_by(name="fronting_alter").first()
            not_fronting = test_db_session.query(Alter).filter_by(name="not_fronting_alter").first()
            
            assert fronting.is_fronting == True
            assert not_fronting.is_fronting == False


def test_init_database_all_modules_enabled_by_default(test_db_session):
    """Test that all modules are enabled by default"""
    from utils.db import ModuleRegistry
    
    mock_session_local = Mock(return_value=test_db_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            modules = test_db_session.query(ModuleRegistry).all()
            
            for module in modules:
                assert module.enabled == True


def test_init_database_calls_init_db(test_db_session):
    """Test that init_database calls init_db to create tables"""
    mock_init_db = Mock()
    mock_session_local = Mock(return_value=test_db_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.init_db', mock_init_db):
        with patch('init_db.SessionLocal', mock_session_local):
            with patch('init_db.TemplateEngine', return_value=mock_template_engine):
                from init_db import init_database
                
                init_database()
                
                mock_init_db.assert_called_once()


def test_init_database_closes_session(test_db_session):
    """Test that init_database always closes the session"""
    mock_session = Mock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.close = Mock()
    
    mock_session_local = Mock(return_value=mock_session)
    mock_template_engine = Mock()
    mock_template_engine.alters_status = {}
    
    with patch('init_db.SessionLocal', mock_session_local):
        with patch('init_db.TemplateEngine', return_value=mock_template_engine):
            from init_db import init_database
            
            init_database()
            
            mock_session.close.assert_called_once()