# Multi-House Application

## Project Overview

This is a modular web application with distinct "houses" (modules) that operate autonomously but integrate through shared components. The application uses FastAPI as its web framework and implements a unique "alter" system that dynamically changes the UI based on which alter is "fronting" (active).

The codebase is organized in the `codebase/` directory to separate the actual implementation from documentation and planning files.

### Architecture

- **Components**: Integration layer that bridges modules with the main application
- **Modules**: Autonomous "houses" with their own resources and data
- **Data Isolation**: Each module maintains its own data while sharing global resources

The project follows a "integration chain" pattern where components serve as bridges between modules and the main application, allowing for clean separation of concerns while maintaining integration.

### Key Features

1. **Modular Architecture**: The application is designed with 3 main modules:
   - Forums: Community discussion platform
   - RTC: Real-time communication
   - Admin: System administration control panel

2. **Component Integration**: A component system handles the integration between modules and the main application, with route conflict validation.

3. **Resource Management**: The system has utilities for validating and loading both local and global resources.

## Building and Running

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Navigate to the codebase directory:
   ```bash
   cd codebase
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

   Or use the Termux startup script:
   ```bash
   ./deploy/termux_start.sh
   ```

### Configuration

The application uses environment variables for configuration defined in `config.py`:

- `DEBUG`: Enable/disable debug mode (default: False)
- `SECRET_KEY`: Secret key for security (default: "your-secret-key-here")
- `VPS_HOST`: Host address (default: "localhost")
- `PORT`: Port to run the application on (default: 8000)
- `DATABASE_URL`: Database connection string (default: "sqlite:///./app.db")
- And more...

## Development Conventions

### Project Structure

```
project/
├── .github/                 # 🛠️ GitHub workflows (test.yml, lint.yml)
├── README.md                # 📄 Project documentation
├── LICENSE                  # 📄 License information
├── QWEN.md                  # 🤖 AI assistant context file
├── plan.tree                # 🗺️ Original architecture plan
├── plans/                   # 📋 Planning documents
└── codebase/                # 🏗️ All actual code files
    ├── main.py              # 🌐 *Core* — FastAPI init + `from components import *`
    ├── config.py            # ⚙️ Global config (DEBUG, SECRET_KEY, VPS_HOST)
    ├── requirements.txt     # 📜 Dependencies
    │
    ├── components/          # ⛓️ *Integration Chain* — bridges modules ↔ app
    │   ├── __init__.py      # ← `setup_components(app)` + route conflict validation
    │   ├── forums_comp.py   # ← `from modules.forums import *`; mounts routes
    │   ├── rtc_comp.py
    │   └── admin_comp.py    # 🔑 Mounts /admin, hooks into module registry
    │
    ├── modules/             # 🏰 *Autonomous Houses* — each self-contained
    │   │
    │   ├── forums/          # 🗣️ House Forums
    │   │   ├── __init__.py  # → exports router, services, *and* resource paths
    │   │   ├── models/      # → Database models (in subdirectory to avoid circular imports)
    │   │   ├── service.py
    │   │   ├── routes/
    │   │   │   ├── threads.py
    │   │   │   └── posts.py
    │   │   │
    │   │   ├── templates/   # 🖼️ *Local Templates* (override global)
    │   │   │   ├── forums/
    │   │   │   │   ├── index.html    # → renders at /forums/ (uses base.html)
    │   │   │   │   └── thread.html
    │   │   │   └── partials/         # Reusable: post_card.html, thread_list.html
    │   │   │
    │   │   ├── static/      # 🎨 *Local Static* (served at /static/forums/)
    │   │   │   ├── css/
    │   │   │   │   └── forums.css    # Scoped: .forums-thread { ... }
    │   │   │   └── js/
    │   │   │       └── forums.js     # HTMX handlers for voting, replies
    │   │   │
    │   │   └── data/        # 📂 *Local Data* — module-private storage
    │   │       ├── cache/   # e.g., thread previews (sqlite or json)
    │   │       └── uploads/ # Forum attachments (symlinked to global uploads/)
    │   │
    │   ├── rtc/             # 📡 House RTC
    │   │   ├── __init__.py
    │   │   ├── connection.py
    │   │   └── routes/
    │   │       └── ws.py
    │   │   ├── templates/
    │   │   │   └── rtc/
    │   │   │       └── chat.html     # WebSocket UI (extends base.html)
    │   │   ├── static/
    │   │   │   └── js/
    │   │   │       └── rtc_client.js # WS connection + message handling
    │   │   └── data/
    │   │       └── sessions.db       # In-memory? No — persistent SQLite (WAL)
    │   │
    │   ├── admin/           # 🔑 House Admin — *Your Control Room*
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── service.py
    │   │   └── routes/
    │   │       ├── dashboard.py
    │   │       ├── modules.py
    │   │       └── logs.py
    │   │   ├── templates/
    │   │   │   └── admin/
    │   │   │       ├── dashboard.html
    │   │   │       └── module_control.html
    │   │   ├── static/
    │   │   │   └── css/
    │   │   │       └── admin.css   # Dark theme, red accents
    │   │   └── data/
    │   │       └── audit.log       # Module toggles, logins — *I timestamp every action*
    │   │
    │   └── _template_module/ # 🎁 *Sacred Blueprint* — copy to create new houses
    │       ├── __init__.py
    │       ├── routes/
    │       ├── templates/
    │       ├── static/
    │       └── data/
    │
    ├── templates/           # 🌍 *Global Templates* — fallbacks & base layout
    │   ├── base.html        # 🏛️ Master: {% block content %}{% endblock %}
    │   ├── index.html       # Home — aggregates enabled modules
    │   └── errors/
    │       ├── 404.html
    │       └── 500.html
    │
    ├── static/              # 🌍 *Global Static* — site-wide assets
    │   ├── css/
    │   │   └── main.css     # Resets, navbar, footer
    │   ├── js/
    │   │   └── htmx.min.js
    │   └── assets/
    │       ├── logo.svg
    │       └── avatars/     # Global alter avatars (fallback if module lacks)
    │
    ├── data/                # 🌍 *Global Data Vault*
    │   ├── registry.db      # 📜 Tracks: module_name, enabled, route_prefix, local_data_path
    │   ├── app.db           # 🗃️ Shared DB (alters, bios, styles — *not* module-private)
    │   ├── app.log          # 📜 Rotated daily
    │   └── uploads/         # 📤 Global upload root — modules symlink here (e.g., forums/uploads → ../uploads/forums)
    │
    ├── utils/
    │   ├── loader.py        # 🔁 Validates local/global paths, loads module resources
    │   ├── db.py
    │   └── security.py
    │
    ├── tests/
    │   ├── conftest.py
    │   ├── test_loader.py   # Tests local/global template resolution
    │   └── test_modules/
    │
    └── deploy/
        └── termux_start.sh
```

### Module Development

Each module is designed to be autonomous and can be developed independently. The basic structure for a new module should include:

1. `__init__.py` - Exports router and services
2. `models/` - Database models (if needed)
3. `routes/` - API routes
4. `templates/` - Module-specific templates that can override global ones
5. `static/` - Module-specific CSS and JavaScript
6. `data/` - Module-private data storage

New modules can use the `_template_module/` as a blueprint.


### Database Models

The application uses SQLAlchemy for database management. The main models are:

1. `ModuleRegistry` - Tracks module status in the system
2. `Alter` - Represents an alter in the system
3. `AuditLog` - Audit log for admin actions
4. Forum models (ForumCategory, ForumThread, ForumPost) in the forums module

## Testing

The project includes basic testing infrastructure, though specific tests need to be implemented. Testing should cover:

- Local/global template resolution
- Database operations
- Module integration
- Template alter switching functionality
- Security functions

## Deployment

The project includes a Termux startup script and GitHub workflows for testing and linting.

## Current Status

The core architecture and framework have been implemented with about 60-70% completion of the full structure planned. The foundation is solid and working:

- ✅ Components integration system is functional
- ✅ Template alter system is working (verified with current alter: "seles")
- ✅ Database initialization works
- ✅ All modules follow the planned import patterns
- ✅ Resource loading and security utilities are in place

Remaining elements include module-specific functionality that can be implemented incrementally.