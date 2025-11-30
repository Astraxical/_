# Deployment and Configuration Plan

## Configuration Management

### Global Configuration File
- **File**: `config.py`
- **Contents**: DEBUG flag, SECRET_KEY, VPS_HOST, and other global settings
- **Purpose**: Centralized configuration accessible to the entire application

### Module Registration Database
- **File**: `data/registry.db`
- **Purpose**: Tracks module status (enabled/disabled), route prefixes, and local data paths
- **Structure**: 
  - module_name (primary key)
  - enabled (boolean)
  - route_prefix (string)
  - local_data_path (string)

### Alter Fronting Configuration
- **File**: `modules/template/data/alters.csv`
- **Purpose**: Tracks which "alter" is currently "fronting" (active)
- **Format**: alter_name,status (e.g., "seles,1"; "dexen,0"; "yuki,0")

## Deployment Strategy

### Termux Deployment
- **Script**: `deploy/termux_start.sh`
- **Purpose**: Start the application in Termux environment
- **Contents**: Environment setup, dependency installation, application start

### Global Assets Management
- **Global Templates**: `templates/` - Base layouts and fallbacks
- **Global Static Assets**: `static/` - Site-wide CSS, JS, and assets
- **Global Data Vault**: `data/` - Shared databases and logs

### Module-Specific Asset Serving
- Local templates override global templates where needed
- Local static assets served at `/static/[module_name]/`
- Module data directories isolated but can link to global locations

## Data Management Strategy

### Global Data
- `data/app.db`: Shared database for non-module-specific data (alters, bios, styles)
- `data/app.log`: Main application log with daily rotation
- `data/uploads/`: Global upload directory with symlinks from modules

### Module Data
- Each module has its own `data/` directory for private storage
- Module data can link to global upload directory as needed
- Persistent SQLite databases for module-specific data (e.g., RTC sessions)

## Environment Considerations

### Development vs Production
- Configuration flags to distinguish environments
- Debug mode with detailed logging vs. production logging
- Static file handling differences

### Security
- Secure secret key management
- Input validation and sanitization
- Access controls for admin module
- Audit logging for sensitive operations

## Performance and Scalability
- Use of SQLite with WAL mode for better concurrency
- Caching strategies for frequently accessed data
- Log rotation to prevent disk space issues
- Efficient template loading and caching

## Backup and Recovery
- Regular backup of registry.db and app.db
- Version control for code changes
- Configuration backup procedures
- Data directory backup strategy