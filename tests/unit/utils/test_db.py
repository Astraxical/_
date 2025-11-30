"""
Unit tests for utils/db.py
"""
import pytest
from datetime import datetime
from sqlalchemy import inspect
from utils.db import (
    Base,
    ModuleRegistry,
    Alter,
    AuditLog,
    init_db
)


class TestModuleRegistryModel:
    """Test ModuleRegistry database model"""
    
    def test_module_registry_creation(self, test_db_session):
        """Test creating a ModuleRegistry instance"""
        module = ModuleRegistry(
            module_name="test_module",
            enabled=True,
            route_prefix="/test",
            local_data_path="modules/test/data"
        )
        test_db_session.add(module)
        test_db_session.commit()
        
        assert module.id is not None
        assert module.module_name == "test_module"
        assert module.enabled is True
        assert module.route_prefix == "/test"
        assert module.local_data_path == "modules/test/data"
    
    def test_module_registry_defaults(self, test_db_session):
        """Test ModuleRegistry default values"""
        module = ModuleRegistry(
            module_name="default_module",
            route_prefix="/default",
            local_data_path="modules/default/data"
        )
        test_db_session.add(module)
        test_db_session.commit()
        
        assert module.enabled is True  # Default should be True
        assert isinstance(module.created_at, datetime)
        assert isinstance(module.updated_at, datetime)
    
    def test_module_registry_unique_name(self, test_db_session):
        """Test that module names must be unique"""
        module1 = ModuleRegistry(
            module_name="unique_test",
            route_prefix="/test1",
            local_data_path="path1"
        )
        test_db_session.add(module1)
        test_db_session.commit()
        
        module2 = ModuleRegistry(
            module_name="unique_test",
            route_prefix="/test2",
            local_data_path="path2"
        )
        test_db_session.add(module2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            test_db_session.commit()
    
    def test_module_registry_query_by_name(self, test_db_session):
        """Test querying module by name"""
        module = ModuleRegistry(
            module_name="forums",
            enabled=True,
            route_prefix="/forums",
            local_data_path="modules/forums/data"
        )
        test_db_session.add(module)
        test_db_session.commit()
        
        found = test_db_session.query(ModuleRegistry).filter(
            ModuleRegistry.module_name == "forums"
        ).first()
        
        assert found is not None
        assert found.module_name == "forums"
    
    def test_module_registry_update(self, test_db_session):
        """Test updating a module registry entry"""
        module = ModuleRegistry(
            module_name="update_test",
            enabled=True,
            route_prefix="/old",
            local_data_path="old/path"
        )
        test_db_session.add(module)
        test_db_session.commit()
        
        old_updated_at = module.updated_at
        
        # Update the module
        module.enabled = False
        module.route_prefix = "/new"
        test_db_session.commit()
        
        assert module.enabled is False
        assert module.route_prefix == "/new"
    
    def test_module_registry_delete(self, test_db_session):
        """Test deleting a module registry entry"""
        module = ModuleRegistry(
            module_name="delete_test",
            route_prefix="/delete",
            local_data_path="delete/path"
        )
        test_db_session.add(module)
        test_db_session.commit()
        
        module_id = module.id
        test_db_session.delete(module)
        test_db_session.commit()
        
        found = test_db_session.query(ModuleRegistry).filter(
            ModuleRegistry.id == module_id
        ).first()
        
        assert found is None
    
    def test_module_registry_tablename(self):
        """Test that tablename is correctly set"""
        assert ModuleRegistry.__tablename__ == "registry"


class TestAlterModel:
    """Test Alter database model"""
    
    def test_alter_creation(self, test_db_session):
        """Test creating an Alter instance"""
        alter = Alter(
            name="seles",
            is_fronting=True,
            bio="Test bio",
            style="purple"
        )
        test_db_session.add(alter)
        test_db_session.commit()
        
        assert alter.id is not None
        assert alter.name == "seles"
        assert alter.is_fronting is True
        assert alter.bio == "Test bio"
        assert alter.style == "purple"
    
    def test_alter_defaults(self, test_db_session):
        """Test Alter default values"""
        alter = Alter(name="dexen")
        test_db_session.add(alter)
        test_db_session.commit()
        
        assert alter.is_fronting is False  # Default should be False
        assert isinstance(alter.created_at, datetime)
        assert isinstance(alter.updated_at, datetime)
    
    def test_alter_unique_name(self, test_db_session):
        """Test that alter names must be unique"""
        alter1 = Alter(name="yuki", is_fronting=False)
        test_db_session.add(alter1)
        test_db_session.commit()
        
        alter2 = Alter(name="yuki", is_fronting=True)
        test_db_session.add(alter2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            test_db_session.commit()
    
    def test_alter_query_by_name(self, test_db_session):
        """Test querying alter by name"""
        alter = Alter(name="test_alter", is_fronting=True)
        test_db_session.add(alter)
        test_db_session.commit()
        
        found = test_db_session.query(Alter).filter(
            Alter.name == "test_alter"
        ).first()
        
        assert found is not None
        assert found.name == "test_alter"
        assert found.is_fronting is True
    
    def test_alter_query_fronting(self, test_db_session):
        """Test querying for fronting alter"""
        alter1 = Alter(name="alter1", is_fronting=False)
        alter2 = Alter(name="alter2", is_fronting=True)
        alter3 = Alter(name="alter3", is_fronting=False)
        
        test_db_session.add_all([alter1, alter2, alter3])
        test_db_session.commit()
        
        fronting = test_db_session.query(Alter).filter(
            Alter.is_fronting == True
        ).all()
        
        assert len(fronting) == 1
        assert fronting[0].name == "alter2"
    
    def test_alter_update(self, test_db_session):
        """Test updating an alter"""
        alter = Alter(name="update_alter", is_fronting=False)
        test_db_session.add(alter)
        test_db_session.commit()
        
        alter.is_fronting = True
        alter.bio = "Updated bio"
        test_db_session.commit()
        
        assert alter.is_fronting is True
        assert alter.bio == "Updated bio"
    
    def test_alter_delete(self, test_db_session):
        """Test deleting an alter"""
        alter = Alter(name="delete_alter")
        test_db_session.add(alter)
        test_db_session.commit()
        
        alter_id = alter.id
        test_db_session.delete(alter)
        test_db_session.commit()
        
        found = test_db_session.query(Alter).filter(
            Alter.id == alter_id
        ).first()
        
        assert found is None
    
    def test_alter_tablename(self):
        """Test that tablename is correctly set"""
        assert Alter.__tablename__ == "alters"


class TestAuditLogModel:
    """Test AuditLog database model"""
    
    def test_audit_log_creation(self, test_db_session):
        """Test creating an AuditLog instance"""
        log = AuditLog(
            action="module_toggle",
            user="admin",
            details="Disabled forums module"
        )
        test_db_session.add(log)
        test_db_session.commit()
        
        assert log.id is not None
        assert log.action == "module_toggle"
        assert log.user == "admin"
        assert log.details == "Disabled forums module"
        assert isinstance(log.timestamp, datetime)
    
    def test_audit_log_defaults(self, test_db_session):
        """Test AuditLog default timestamp"""
        log = AuditLog(action="test_action", user="testuser")
        test_db_session.add(log)
        test_db_session.commit()
        
        assert isinstance(log.timestamp, datetime)
        assert log.timestamp is not None
    
    def test_audit_log_query_by_user(self, test_db_session):
        """Test querying audit logs by user"""
        log1 = AuditLog(action="action1", user="user1")
        log2 = AuditLog(action="action2", user="user1")
        log3 = AuditLog(action="action3", user="user2")
        
        test_db_session.add_all([log1, log2, log3])
        test_db_session.commit()
        
        user1_logs = test_db_session.query(AuditLog).filter(
            AuditLog.user == "user1"
        ).all()
        
        assert len(user1_logs) == 2
    
    def test_audit_log_query_by_action(self, test_db_session):
        """Test querying audit logs by action"""
        log1 = AuditLog(action="login", user="user1")
        log2 = AuditLog(action="logout", user="user1")
        log3 = AuditLog(action="login", user="user2")
        
        test_db_session.add_all([log1, log2, log3])
        test_db_session.commit()
        
        login_logs = test_db_session.query(AuditLog).filter(
            AuditLog.action == "login"
        ).all()
        
        assert len(login_logs) == 2
    
    def test_audit_log_with_details(self, test_db_session):
        """Test audit log with detailed information"""
        details = "Changed module status from enabled to disabled"
        log = AuditLog(
            action="config_change",
            user="admin",
            details=details
        )
        test_db_session.add(log)
        test_db_session.commit()
        
        assert log.details == details
    
    def test_audit_log_without_details(self, test_db_session):
        """Test audit log without details"""
        log = AuditLog(action="simple_action", user="user")
        test_db_session.add(log)
        test_db_session.commit()
        
        assert log.details is None
    
    def test_audit_log_tablename(self):
        """Test that tablename is correctly set"""
        assert AuditLog.__tablename__ == "audit_log"


class TestDatabaseInitialization:
    """Test database initialization"""
    
    def test_init_db_creates_tables(self, test_db_engine):
        """Test that init_db creates all tables"""
        # Clear existing tables
        Base.metadata.drop_all(bind=test_db_engine)
        
        # Initialize database
        init_db()
        
        # Check that tables exist
        inspector = inspect(test_db_engine)
        table_names = inspector.get_table_names()
        
        assert "registry" in table_names
        assert "alters" in table_names
        assert "audit_log" in table_names
    
    def test_init_db_idempotent(self, test_db_engine):
        """Test that init_db can be called multiple times safely"""
        init_db()
        init_db()  # Should not raise error
        
        inspector = inspect(test_db_engine)
        table_names = inspector.get_table_names()
        
        assert "registry" in table_names
        assert "alters" in table_names
        assert "audit_log" in table_names


class TestDatabaseRelationships:
    """Test database relationships and constraints"""
    
    def test_multiple_modules_independent(self, test_db_session):
        """Test that multiple modules can exist independently"""
        modules = [
            ModuleRegistry(module_name="forums", route_prefix="/forums", local_data_path="forums/data"),
            ModuleRegistry(module_name="rtc", route_prefix="/rtc", local_data_path="rtc/data"),
            ModuleRegistry(module_name="admin", route_prefix="/admin", local_data_path="admin/data")
        ]
        
        test_db_session.add_all(modules)
        test_db_session.commit()
        
        all_modules = test_db_session.query(ModuleRegistry).all()
        assert len(all_modules) == 3
    
    def test_multiple_alters(self, test_db_session):
        """Test that multiple alters can exist"""
        alters = [
            Alter(name="seles", is_fronting=True),
            Alter(name="dexen", is_fronting=False),
            Alter(name="yuki", is_fronting=False)
        ]
        
        test_db_session.add_all(alters)
        test_db_session.commit()
        
        all_alters = test_db_session.query(Alter).all()
        assert len(all_alters) == 3