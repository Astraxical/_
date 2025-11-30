# Module Architecture Plan

## Module Principles
Each module operates as an autonomous "house" with its own:
- Business logic (models, services)
- Web interface (routes, templates, static assets)
- Data storage (local data directory)
- Resource management (templates, static files, data)

## Module Directory Structure Template
```
modules/[module_name]/
├── __init__.py            # Exports router, services, and resource paths
├── models.py              # Database models specific to the module
├── service.py             # Business logic and data processing
├── routes/                # Route handlers
│   ├── [feature1].py
│   └── [feature2].py
├── templates/             # Local templates (can override global templates)
│   ├── [module_name]/
│   │   ├── index.html     # Module-specific templates
│   │   └── [page].html
│   └── partials/          # Reusable template components
├── static/                # Module-specific assets
│   ├── css/
│   │   └── [module_name].css
│   └── js/
│       └── [module_name].js
└── data/                  # Module-private data storage
    ├── cache/
    └── uploads/           # Symlinked to global uploads/
```

## Individual Module Plans

### 1. Forums Module
**Purpose**: Community discussion platform
- **Models**: Thread, Post, Category models
- **Services**: Thread management, post voting, categorization
- **Routes**: `/forums/`, `/forums/thread/{id}`, `/forums/category/{id}`
- **Templates**: Thread display, post creation, category browsing
- **Static**: CSS for thread layout, JS for voting and reply handling
- **Data**: Thread cache, uploaded attachments

### 2. RTC (Real-Time Communication) Module
**Purpose**: Real-time chat and communication
- **Models**: Connection, Message, Session models
- **Services**: WebSocket connection management, message broadcasting
- **Routes**: WebSocket endpoints for real-time communication
- **Templates**: Chat interface with WebSocket UI
- **Static**: Client-side JavaScript for WebSocket handling
- **Data**: Session database (SQLite with WAL for concurrency)

### 3. Template Module
**Purpose**: The system's face - manages alter-specific rendering
- **Models**: Alter status, template overrides
- **Services**: `render_alter()` function for alter-specific rendering
- **Routes**: None directly, used by other modules
- **Templates**: Per-alter templates (seles/, dexen/, yuki/ overrides)
- **Static**: Alter-specific CSS files
- **Data**: Alter state files, alters.csv for fronting status

### 4. Admin Module
**Purpose**: Control room for system administration
- **Models**: User, Permission, AuditLog models
- **Services**: Authentication, authorization, audit logging
- **Routes**: Dashboard, module control, logs
- **Templates**: Admin interface with dark theme
- **Static**: Admin-specific CSS and JS
- **Data**: Audit logs, module configuration

## Module Communication
- Modules do not communicate directly with each other
- Instead, communication happens through:
  - Shared global templates
  - Global static assets
  - Global data (app.db, registry.db)
  - The component integration layer

## Module Registration and Discovery
- Each module's `__init__.py` exports its router and services
- Components import from modules using star imports
- The registry.db tracks module status (enabled/disabled)
- Module routes are mounted by components at startup

## Module Data Isolation
- Private data stored in module's data/ directory
- Global data stored in project's data/ directory
- Module data can be symlinked to global locations when appropriate
- Database tables can be local (module-specific) or global (shared)

## Template Override System
- Modules can override global templates for their sections
- Template alter system allows different UI based on which "alter" is fronting
- Local templates take precedence over global templates
- Fallback to global templates when local ones don't exist