# Utility and Testing Plan

## Utility Functions

### Loader Utility (`utils/loader.py`)
- **Purpose**: Validates and loads module resources (templates, static assets)
- **Features**:
  - Path validation for local and global resources
  - Module resource loading with fallback mechanisms
  - Template resolution with override hierarchy
  - Static asset path management

### Database Utility (`utils/db.py`)
- **Purpose**: Common database operations and connection management
- **Features**:
  - Connection pooling
  - Common query patterns
  - Transaction management
  - Migration helpers

### Security Utility (`utils/security.py`)
- **Purpose**: Security-related functions across the application
- **Features**:
  - Authentication helpers
  - Authorization utilities
  - Input sanitization
  - Password hashing
  - CSRF protection

## Testing Strategy

### Test Structure
```
tests/
├── conftest.py            # Pytest configuration and fixtures
├── test_loader.py         # Tests local/global template resolution
└── test_modules/          # Module-specific tests
    ├── test_forums.py
    ├── test_rtc.py
    ├── test_template.py
    └── test_admin.py
```

### Testing Types

#### Unit Tests
- Test individual functions and classes
- Focus on business logic in service.py files
- Test utility functions in isolation

#### Integration Tests
- Test module-component integration
- Verify route mounting and conflict detection
- Test template override behavior
- Validate data access patterns

#### End-to-End Tests
- Full application flow testing
- Template alter system validation
- Cross-module interaction verification
- Static asset serving checks

### Test Coverage Focus Areas
- Local vs global template resolution
- Module enable/disable functionality
- Template alter system behavior
- Data isolation between modules
- Route conflict validation
- Security measures implementation

### CI/CD Pipeline
- **GitHub Actions**: `.github/workflows/`
  - `test.yml`: Automated pytest execution
  - `lint.yml`: Code quality checks (ruff)
  - Enforce no star imports outside components/* (except where necessary)

### Linting and Code Quality
- Use ruff for Python linting
- Enforce consistent code style
- Prevent import anti-patterns outside components
- Ensure security best practices

## Development Utilities

### Global Template Resolution
- Verify local templates properly override global templates
- Test fallback behavior when local templates don't exist
- Validate alter-specific template loading

### Module Registration Validation
- Test module registration in registry.db
- Verify route mounting behavior
- Validate module enable/disable functionality

### Data Access Testing
- Test isolation between module data
- Verify global data access patterns
- Validate symlink behavior for uploads
- Check database concurrency handling

## Quality Assurance Process
1. Pre-commit hooks for code quality
2. Automated testing on all PRs
3. Code review checklist for architecture compliance
4. Performance testing for critical paths
5. Security scanning for potential vulnerabilities