# Test Suite Documentation

This directory contains comprehensive unit tests for the Multi-House Application codebase.

## Running Tests

### Run all tests
pytest

### Run with coverage
pytest --cov=codebase --cov-report=html

### Run specific test file
pytest tests/unit/utils/test_security.py

### Run with verbose output
pytest -v

## Test Coverage

The test suite covers:
- Utility modules (loader, security, db)
- Component integration layer
- Module initialization
- Configuration handling
- Database initialization
- Main application setup