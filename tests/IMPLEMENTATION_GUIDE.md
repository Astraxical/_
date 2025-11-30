# Unit Tests Implementation Guide

## Quick Start

### Running All New Tests
```bash
cd /home/jailuser/git
./run_new_tests.sh
```

### Running Individual Test Suites
```bash
# Template Engine tests (core functionality)
pytest tests/unit/modules/test_template_engine.py -v

# Template Component tests (integration layer)
pytest tests/unit/components/test_template_comp.py -v

# Template Routes tests (API endpoints)
pytest tests/unit/modules/test_template_routes.py -v

# Main application tests (with rate limiting)
pytest tests/unit/test_main_updated.py -v

# Database initialization tests
pytest tests/unit/test_init_db_updated.py -v
```

### Running with Coverage Report
```bash
pytest tests/unit/modules/test_template_engine.py \
       tests/unit/modules/test_template_routes.py \
       tests/unit/components/test_template_comp.py \
       --cov=codebase/modules/template \
       --cov=codebase/components/template_comp \
       --cov-report=html \
       --cov-report=term
```

## Test Structure Overview

### 1. Template Engine Tests (`test_template_engine.py`)
**Purpose**: Test the core TemplateEngine class that manages alter system

**Key Test Classes**:
- `TestTemplateEngineInitialization` - CSV loading, alter detection
- `TestTemplateSetup` - Template path resolution
- `TestAlterSwitching` - Alter switching logic
- `TestTemplateRendering` - Context injection and rendering
- `TestCSVPersistence` - File I/O operations
- `TestEdgeCases` - Boundary conditions and error states

**Critical Tests**:
```python
# Tests alter switching updates all state correctly
test_switch_alter_success()

# Tests CSV is created with defaults if missing
test_init_creates_csv_if_not_exists()

# Tests template context includes alter information
test_render_includes_alter_context()
```

### 2. Template Component Tests (`test_template_comp.py`)
**Purpose**: Test integration between template module and FastAPI app

**Key Test Classes**:
- `TestTemplateComponentSetup` - Router mounting and metadata
- `TestTemplateComponentIntegration` - Multiple setup scenarios

**Critical Tests**:
```python
# Tests router is properly included in app
test_setup_template_includes_router()

# Tests correct metadata is returned
test_setup_template_returns_correct_metadata()
```

### 3. Template Routes Tests (`test_template_routes.py`)
**Purpose**: Test API endpoints for alter management

**Key Test Classes**:
- `TestAlterSwitchEndpoint` - Switch alter API
- `TestAlterStatusEndpoint` - Status query API
- `TestRouterConfiguration` - Router setup

**Critical Tests**:
```python
# Tests successful alter switch via API
test_switch_alter_success()

# Tests status endpoint returns current state
test_get_alter_status()

# Tests invalid alter names are rejected
test_switch_alter_failure()
```

### 4. Main Application Tests (`test_main_updated.py`)
**Purpose**: Test updated main.py with rate limiting and template engine

**Key Test Classes**:
- `TestAppInitialization` - Rate limiter setup
- `TestRootRouteWithTemplateEngine` - Template rendering on /
- `TestRateLimiting` - Rate limit configuration
- `TestComponentsSetup` - Component integration

**Critical Tests**:
```python
# Tests rate limiter is initialized
test_app_has_rate_limiter()

# Tests root route uses template engine
test_root_route_uses_template_engine()

# Tests exception handler is registered
test_rate_limit_exception_handler_registered()
```

### 5. Database Init Tests (`test_init_db_updated.py`)
**Purpose**: Test database initialization with alter/module updates

**Key Test Classes**:
- `TestInitDatabaseWithAlterUpdates` - Alter upsert logic
- `TestInitDatabaseWithModuleUpdates` - Module upsert logic
- `TestErrorHandling` - Rollback and error recovery
- `TestSuccessPath` - Happy path validation

**Critical Tests**:
```python
# Tests existing alters are updated not recreated
test_updates_existing_alters()

# Tests new modules are registered
test_registers_all_required_modules()

# Tests database rolls back on error
test_rollback_on_exception()
```

## Test Patterns and Best Practices

### Mocking Pattern
```python
@patch('module.dependency')
def test_function(self, mock_dependency):
    """Test description"""
    mock_dependency.return_value = expected_value
    
    result = function_under_test()
    
    assert result == expected_value
    mock_dependency.assert_called_once()
```

### FastAPI Testing Pattern
```python
from fastapi.testclient import TestClient

def test_endpoint():
    """Test API endpoint"""
    client = TestClient(app)
    response = client.get('/endpoint')
    
    assert response.status_code == 200
    assert response.json()['key'] == 'value'
```

### Database Testing Pattern
```python
@patch('module.SessionLocal')
def test_database_operation(self, mock_session):
    """Test database interaction"""
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    
    function_under_test()
    
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()
```

## Coverage Goals

### Current Coverage Targets
- **Template Engine**: 95%+ coverage (core business logic)
- **Template Routes**: 90%+ coverage (API endpoints)
- **Main Application**: 85%+ coverage (integration points)
- **Database Init**: 90%+ coverage (data persistence)

### Running Coverage Analysis
```bash
# Generate HTML coverage report
pytest tests/unit/ --cov=codebase --cov-report=html

# View report
open htmlcov/index.html
```

## Common Issues and Solutions

### Issue: Import Errors
**Solution**: Ensure codebase is in Python path
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))
```

### Issue: Mock Not Working
**Solution**: Patch at the point of use, not definition
```python
# Wrong
@patch('original.module.function')

# Right
@patch('using.module.function')
```

### Issue: Database Tests Failing
**Solution**: Mock SessionLocal, not the database
```python
@patch('module.SessionLocal')
def test_db(self, mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db
```

## Adding New Tests

### Template for New Test Class
```python
class TestNewFeature:
    """Test suite for new feature."""
    
    def setup_method(self):
        """Setup before each test."""
        pass
    
    def teardown_method(self):
        """Cleanup after each test."""
        pass
    
    @patch('module.dependency')
    def test_happy_path(self, mock_dep):
        """Test normal operation."""
        # Arrange
        mock_dep.return_value = expected
        
        # Act
        result = function()
        
        # Assert
        assert result == expected
        mock_dep.assert_called_once()
    
    def test_edge_case(self):
        """Test boundary condition."""
        result = function(edge_case_input)
        assert result is not None
    
    def test_error_handling(self):
        """Test error condition."""
        with pytest.raises(ExpectedException):
            function(invalid_input)
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r codebase/requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=codebase
```

## Maintenance

### Regular Updates
- Run tests before each commit
- Update tests when changing functionality
- Add tests for new features
- Remove tests for deprecated features

### Review Checklist
- [ ] All tests pass
- [ ] Coverage meets targets
- [ ] No flaky tests
- [ ] Clear test names
- [ ] Proper mocking
- [ ] Edge cases covered
- [ ] Error handling tested

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Support

For issues or questions about the tests:
1. Check test output for specific error
2. Review this guide for common solutions
3. Check existing tests for patterns
4. Refer to TEST_COVERAGE_SUMMARY.md for test details