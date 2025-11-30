"""
Initialize the database with default values
"""
from utils.db import init_db, SessionLocal, ModuleRegistry, Alter
from modules.template.engine import TemplateEngine

def init_database():
    # Initialize database tables
    """
    Initialize the database schema and seed default alters and module registrations.

    Ensures database tables exist, adds missing alter entries based on TemplateEngine.alters_status, registers a predefined set of modules in ModuleRegistry if they are absent, and commits the changes. On error the transaction is rolled back; the database session is always closed.
    """
    init_db()

    db = SessionLocal()

    try:
        # Initialize default alters
        template_engine = TemplateEngine()
        for alter_name, is_active in template_engine.alters_status.items():
            existing_alter = db.query(Alter).filter(Alter.name == alter_name).first()
            if not existing_alter:
                alter = Alter(
                    name=alter_name,
                    is_fronting=is_active
                )
                db.add(alter)
            else:
                # Update existing alter if needed
                existing_alter.is_fronting = is_active

        # Initialize default modules in registry
        modules_to_register = [
            {"module_name": "template", "enabled": True, "route_prefix": "/template", "local_data_path": "modules/template/data"},
            {"module_name": "admin", "enabled": True, "route_prefix": "/admin", "local_data_path": "modules/admin/data"},
            {"module_name": "forums", "enabled": True, "route_prefix": "/forums", "local_data_path": "modules/forums/data"},
            {"module_name": "rtc", "enabled": True, "route_prefix": "/rtc", "local_data_path": "modules/rtc/data"}
        ]

        for module_data in modules_to_register:
            existing_module = db.query(ModuleRegistry).filter(ModuleRegistry.module_name == module_data["module_name"]).first()
            if not existing_module:
                module = ModuleRegistry(**module_data)
                db.add(module)
            else:
                # Update existing module if needed
                existing_module.enabled = module_data["enabled"]
                existing_module.route_prefix = module_data["route_prefix"]
                existing_module.local_data_path = module_data["local_data_path"]

        db.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()