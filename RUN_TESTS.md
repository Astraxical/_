# Running the Generated Tests

## Quick Start

### Run All Tests
```bash
cd /home/jailuser/git
pytest tests/unit/ -v
```

### Run Specific Module Tests

**Template Module:**
```bash
pytest tests/unit/modules/template/ -v
```

**Admin Module:**
```bash
pytest tests/unit/modules/admin/ -v
```

**Forums Module:**
```bash
pytest tests/unit/modules/forums/ -v
```

**RTC Module:**
```bash
pytest tests/unit/modules/rtc/ -v
```

**Component Tests:**
```bash
pytest tests/unit/components/test_template_comp.py -v
```

**Utility Tests:**
```bash
pytest tests/unit/utils/test_loader_comprehensive.py -v
pytest tests/unit/utils/test_security_comprehensive.py -v
```

### Run with Coverage

**Generate coverage report:**
```bash
pytest tests/unit/ --cov=codebase --cov-report=html --cov-report=term
```

**View coverage report:**
```bash
# Open htmlcov/index.html in a browser
```

### Run Specific Test Classes

```bash
# Template Engine initialization tests
pytest tests/unit/modules/template/test_engine.py::TestTemplateEngineInitialization -v

# Alter switching tests
pytest tests/unit/modules/template/test_engine.py::TestSwitchAlter -v

# Admin dashboard tests
pytest tests/unit/modules/admin/test_routes_dashboard.py::TestAdminDashboard -v

# WebSocket tests
pytest tests/unit/modules/rtc/test_routes_ws.py::TestWebSocketEndpoint -v
```

### Run with Markers

**Run only unit tests:**
```bash
pytest tests/unit/ -m unit -v
```

**Run async tests:**
```bash
pytest tests/unit/modules/rtc/test_routes_ws.py -m asyncio -v
```

### Debugging Failed Tests

**Run with verbose output:**
```bash
pytest tests/unit/ -vv
```

**Stop on first failure:**
```bash
pytest tests/unit/ -x
```

**Show local variables on failure:**
```bash
pytest tests/unit/ -l
```

**Run last failed tests:**
```bash
pytest tests/unit/ --lf
```

### Performance Testing

**Show slowest tests:**
```bash
pytest tests/unit/ --durations=10
```

## Test File Organization