#!/bin/bash

echo "Running dashboard performance tests..."

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the performance tests
# The --capture=no flag ensures print statements in the tests are shown
# The --ignore-glob allows us to run specific tests or all tests depending on need
pytest performance_tests/dashboard_load_test.py --capture=no

if [ $? -eq 0 ]; then
    echo "Performance tests passed successfully."
else
    echo "Performance tests failed. Check the logs above for details."
    exit 1
fi
