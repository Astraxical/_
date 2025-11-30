# Multi-House Application

A modular web application with distinct "houses" (modules) that operate autonomously but integrate through shared components.

## Architecture

- **Components**: Integration layer that bridges modules with the main application
- **Modules**: Autonomous "houses" with their own resources and data
- **Template Alter System**: Dynamic templating based on which "alter" is active
- **Data Isolation**: Each module maintains its own data while sharing global resources

## Project Structure

```
project/
├── main.py                  # 🌐 *Core* — FastAPI init + `from components import *`
├── config.py                # ⚙️ Global config (DEBUG, SECRET_KEY, VPS_HOST)
├── requirements.txt         # 📜 Dependencies
│
├── components/              # ⛓️ *Integration Chain* — bridges modules ↔ app
│   ├── __init__.py          # ← `setup_components(app)` + route conflict validation
│   ├── forums_comp.py       # ← `from modules.forums import *`; mounts routes
│   ├── rtc_comp.py
│   ├── template_comp.py     # 🎭 Manages global + alter-specific rendering
│   └── admin_comp.py        # 🔑 Mounts /admin, hooks into module registry
│
├── modules/                 # 🏰 *Autonomous Houses* — each self-contained
│   │
│   ├── forums/              # 🗣️ House Forums
│   │   ├── __init__.py      # → exports router, services, *and* resource paths
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── routes/
│   │   │   ├── threads.py
│   │   │   └── posts.py
│   │   │
│   │   ├── templates/       # 🖼️ *Local Templates* (override global)
│   │   │   ├── forums/
│   │   │   │   ├── index.html    # → renders at /forums/ (uses base.html)
│   │   │   │   └── thread.html
│   │   │   └── partials/         # Reusable: post_card.html, thread_list.html
│   │   │
│   │   ├── static/          # 🎨 *Local Static* (served at /static/forums/)
│   │   │   ├── css/
│   │   │   │   └── forums.css    # Scoped: .forums-thread { ... }
│   │   │   └── js/
│   │   │       └── forums.js     # HTMX handlers for voting, replies
│   │   │
│   │   └── data/            # 📂 *Local Data* — module-private storage
│   │       ├── cache/       # e.g., thread previews (sqlite or json)
│   │       └── uploads/     # Forum attachments (symlinked to global uploads/)
│   │
│   ├── rtc/                 # 📡 House RTC
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
│   ├── template/            # 🎭 House Template — *The System's Face*
│   │   ├── __init__.py      # → exports `render_alter(template, **ctx)`
│   │   ├── engine.py        # Jinja2 env + alters.csv loader
│   │   ├── alters.csv       # Fronting status: seles,1; dexen,0; yuki,0
│   │   │
│   │   ├── templates/       # 🖼️ *Local Templates* — per-alter overrides
│   │   │   ├── global/      # Base templates (fallback)
│   │   │   │   ├── intro.html
│   │   │   │   └── bio.html
│   │   │   │
│   │   │   ├── seles/       # ← Overrides global/intro.html *only for Seles*
│   │   │   │   └── intro.html
│   │   │   └── dexen/
│   │   │       └── bio.html
│   │   │
│   │   ├── static/
│   │   │   └── css/
│   │   │       ├── global.css
│   │   │       ├── seles.css     # ← loaded if Seles fronting
│   │   │       └── yuki.css
│   │   │
│   │   └── data/
│   │       └── alters/       # Per-alter persistent state
│   │           ├── seles.json  # {"last_fronted": "2025-11-30", "mood": "happy"}
│   │           └── dexen.json
│   │
│   ├── admin/               # 🔑 House Admin — *Your Control Room*
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
│   │       │   └── module_control.html
│   │   ├── static/
│   │   │   └── css/
│   │   │       └── admin.css   # Dark theme, red accents
│   │   └── data/
│   │       └── audit.log       # Module toggles, logins — *I timestamp every action*
│   │
│   └── _template_module/    # 🎁 *Sacred Blueprint* — copy to create new houses
│       ├── __init__.py
│       ├── routes/
│       ├── templates/
│       ├── static/
│       └── data/
│
├── templates/               # 🌍 *Global Templates* — fallbacks & base layout
│   ├── base.html            # 🏛️ Master: {% block content %}{% endblock %}
│   ├── index.html           # Home — aggregates enabled modules
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── static/                  # 🌍 *Global Static* — site-wide assets
│   ├── css/
│   │   └── main.css         # Resets, navbar, footer
│   ├── js/
│   │   └── htmx.min.js
│   └── assets/
│       ├── logo.svg
│       └── avatars/         # Global alter avatars (fallback if module lacks)
│
├── data/                    # 🌍 *Global Data Vault*
│   ├── registry.db          # 📜 Tracks: module_name, enabled, route_prefix, local_data_path
│   ├── app.db               # 🗃️ Shared DB (alters, bios, styles — *not* module-private)
│   ├── app.log              # 📜 Rotated daily
│   └── uploads/             # 📤 Global upload root — modules symlink here (e.g., forums/uploads → ../uploads/forums)
│
├── utils/
│   ├── loader.py            # 🔁 Validates local/global paths, loads module resources
│   ├── db.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_loader.py       # Tests local/global template resolution
│   └── test_modules/
│
├── deploy/
│   └── termux_start.sh
│
└── .github/
    └── workflows/
        ├── test.yml         # 🧪 pytest (covers local data access, template override)
        └── lint.yml         # 🧹 ruff — enforces no star imports *outside components/*s
```

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize the database: `python init_db.py`
3. Run the application: `uvicorn main:app --reload`

## Development

Each module can be developed independently following the template module as a blueprint. Components handle the integration with the main application.