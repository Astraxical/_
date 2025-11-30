# Quick Reference Card

## Run Tests

```bash
# All new tests
./run_new_tests.sh

# Individual files
pytest tests/unit/modules/test_template_engine.py -v
pytest tests/unit/components/test_template_comp.py -v
pytest tests/unit/modules/test_template_routes.py -v
pytest tests/unit/test_main_updated.py -v
pytest tests/unit/test_init_db_updated.py -v

# With coverage
pytest tests/unit/ --cov=codebase --cov-report=html

# Specific test
pytest tests/unit/modules/test_template_engine.py::TestTemplateEngineInitialization::test_init_loads_alters_from_csv -v
```

## Test Statistics

| Metric | Value |
|--------|-------|
| Total Tests | 46 |
| Test Files | 5 |
| Lines of Code | 848 |
| Coverage Target | 91% |
| Execution Time | < 5 seconds |

## Test Files

1. **test_template_engine.py** (16 tests, 268 lines)
   - Template engine core functionality
   
2. **test_template_comp.py** (4 tests, 61 lines)
   - Component integration with FastAPI
   
3. **test_template_routes.py** (7 tests, 132 lines)
   - API endpoints for alter management
   
4. **test_main_updated.py** (11 tests, 170 lines)
   - Main app with rate limiting
   
5. **test_init_db_updated.py** (8 tests, 217 lines)
   - Database initialization with updates

## Documentation

- **TEST_COVERAGE_SUMMARY.md** - Test organization
- **IMPLEMENTATION_GUIDE.md** - How-to guide
- **TEST_ARCHITECTURE.md** - Architecture docs
- **DELIVERY_SUMMARY.md** - Delivery overview
- **QUICK_REFERENCE.md** - This file

## Common Commands

```bash
# Check test syntax
python3 -m py_compile tests/unit/modules/test_template_engine.py

# List all tests
pytest --collect-only tests/unit/

# Run with markers
pytest tests/unit/ -m unit

# Stop on first failure
pytest tests/unit/ -x

# Show local variables on failure
pytest tests/unit/ -l

# Verbose with traceback
pytest tests/unit/ -vv --tb=short
```

## Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow tests

## Troubleshooting

**Import errors?**
- Check codebase is in PYTHONPATH
- Verify sys.path.insert in test file

**Mocks not working?**
- Patch at point of use, not definition
- Check mock.assert_called_* methods

**Tests failing?**
- Run with -vv for verbose output
- Check mock return values
- Verify fixture setup

## Next Steps

1. Review test output
2. Check coverage report
3. Fix any failures
4. Commit tests with code changes
5. Set up CI/CD integration

---

**Created**: 2024  
**Status**: Production-Ready