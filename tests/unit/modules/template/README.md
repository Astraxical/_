# Template Module Tests

This directory contains comprehensive unit tests for the template module, which provides the alter system and template rendering functionality.

## Test Files

### `test_engine.py`
Tests for the core `TemplateEngine` class that manages alter-based template rendering.

**Coverage:**
- CSV file loading and creation
- Template path resolution
- Alter switching functionality
- Context injection for rendering
- State persistence

**Key Test Classes:**
- `TestTemplateEngineInit` - Initialization
- `TestTemplateEngineSetupTemplates` - Template path configuration
- `TestTemplateEngineRender` - Rendering with context
- `TestTemplateEngineSwitchAlter` - Alter switching
- `TestTemplateEngineSaveAltersStatus` - CSV persistence
- `TestTemplateEngineEdgeCases` - Edge cases

### `test_template_module_init.py`
Tests for the template module initialization and router setup.

**Coverage:**
- Router configuration
- Module metadata
- Route patterns
- Integration points

### `routes/test_alter.py`
Tests for the alter switching and status API endpoints.

**Coverage:**
- Alter switching endpoint
- Status retrieval endpoint
- Error handling
- Edge cases

## Running Tests

```bash
# Run all template module tests
pytest tests/unit/modules/template/ -v

# Run specific test file
pytest tests/unit/modules/template/test_engine.py -v

# Run with coverage
pytest tests/unit/modules/template/ --cov=codebase/modules/template --cov-report=html

# Run specific test class
pytest tests/unit/modules/template/test_engine.py::TestTemplateEngineInit -v
```

## Test Statistics

- **Total test methods:** 49
- **Test classes:** 13
- **Files covered:** 3 (engine.py, __init__.py, routes/alter.py)
- **Coverage:** 100% of new functionality