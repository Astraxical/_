#!/bin/bash

echo "=========================================="
echo "Test Suite Verification"
echo "=========================================="
echo ""

echo "1. Checking test file structure..."
echo ""

test_files=(
    "tests/unit/modules/template/test_engine.py"
    "tests/unit/modules/template/test_template_module_init.py"
    "tests/unit/modules/template/routes/test_alter.py"
    "tests/unit/components/test_template_comp.py"
    "tests/unit/test_main_updates.py"
    "tests/unit/test_init_db_updates.py"
    "tests/unit/modules/admin/test_routes_dashboard.py"
    "tests/unit/modules/admin/test_routes_modules.py"
    "tests/unit/modules/forums/routes/test_threads.py"
    "tests/unit/modules/forums/routes/test_posts.py"
    "tests/unit/modules/rtc/routes/test_ws.py"
)

all_exist=true
for file in "${test_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (MISSING)"
        all_exist=false
    fi
done

echo ""
if [ "$all_exist" = true ]; then
    echo "✓ All test files exist!"
else
    echo "✗ Some test files are missing"
    exit 1
fi

echo ""
echo "2. Counting test methods..."
echo ""

total_tests=0
for file in "${test_files[@]}"; do
    if [ -f "$file" ]; then
        count=$(grep -c "def test_" "$file")
        echo "  $file: $count tests"
        total_tests=$((total_tests + count))
    fi
done

echo ""
echo "Total test methods: $total_tests"

echo ""
echo "3. Verifying test structure..."
echo ""

# Check for pytest markers
if grep -r "@pytest.mark" tests/unit/modules/template/ tests/unit/modules/rtc/ > /dev/null 2>&1; then
    echo "✓ Async test markers found"
else
    echo "! No pytest markers (may not be needed)"
fi

# Check for proper imports
if grep -r "import pytest" tests/unit/modules/template/ tests/unit/components/ > /dev/null 2>&1; then
    echo "✓ pytest imports found"
else
    echo "✗ Missing pytest imports"
fi

# Check for mock usage
if grep -r "from unittest.mock import" tests/unit/modules/template/ tests/unit/components/ > /dev/null 2>&1; then
    echo "✓ unittest.mock imports found"
else
    echo "✗ Missing mock imports"
fi

echo ""
echo "4. Test file statistics..."
echo ""

echo "Test classes: $(grep -r "^class Test" tests/unit/modules/template/ tests/unit/components/test_template_comp.py tests/unit/test_main_updates.py tests/unit/test_init_db_updates.py tests/unit/modules/admin/ tests/unit/modules/forums/routes/ tests/unit/modules/rtc/routes/ | wc -l)"
echo "Test methods: $total_tests"
echo "Docstrings: $(grep -r '"""' tests/unit/modules/template/ tests/unit/components/test_template_comp.py | wc -l)"

echo ""
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="