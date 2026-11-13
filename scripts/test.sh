
#!/bin/bash

# Move to the project root directory
cd "$(dirname "$0")/.." || exit 1

echo "=========================================="
echo "       RUNNING PROJECT TESTS"
echo "=========================================="

python -m pytest -v

if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed. Check the output above."
    exit 1
fi
