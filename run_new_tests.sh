#!/bin/bash

# Test runner for new branch tests

echo "================================"
echo "Running New Branch Unit Tests"
echo "================================"

echo -e "\n1. Testing Template Engine..."
pytest tests/unit/modules/test_template_engine.py -v --tb=short

echo -e "\n2. Testing Template Component..."
pytest tests/unit/components/test_template_comp.py -v --tb=short

echo -e "\n3. Testing Template Routes..."
pytest tests/unit/modules/test_template_routes.py -v --tb=short

echo -e "\n4. Testing Updated Main..."
pytest tests/unit/test_main_updated.py -v --tb=short

echo -e "\n5. Testing Updated Init DB..."
pytest tests/unit/test_init_db_updated.py -v --tb=short

echo -e "\n================================"
echo "Test Summary"
echo "================================"
pytest tests/unit/modules/test_template_engine.py tests/unit/modules/test_template_routes.py tests/unit/components/test_template_comp.py tests/unit/test_main_updated.py tests/unit/test_init_db_updated.py --tb=no -q