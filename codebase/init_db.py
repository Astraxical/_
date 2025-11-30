"""
Initialize the database with default values
"""
from utils.db import init_db, SessionLocal, ModuleRegistry

def init_database():
    # Initialize database tables
    """
    Initialize the database schema and seed default modules in the registry.

    Ensures database tables exist, registers a predefined set of modules in ModuleRegistry if they are absent, and commits the changes. On error the transaction is rolled back; the database session is always closed.
    """
    init_db()

    db = SessionLocal()

    try:
        # Initialize default modules in registry
        modules_to_register = [
            {"module_name": "admin", "enabled": True, "route_prefix": "/admin", "local_data_path": "modules/admin/data"},
            {"module_name": "forums", "enabled": True, "route_prefix": "/forums", "local_data_path": "modules/forums/data"},
            {"module_name": "rtc", "enabled": True, "route_prefix": "/rtc", "local_data_path": "modules/rtc/data"}
        ]

        for module_data in modules_to_register:
            existing_module = db.query(ModuleRegistry).filter(ModuleRegistry.module_name == module_data["module_name"]).first()
            if not existing_module:
                module = ModuleRegistry(**module_data)
                db.add(module)

        db.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()