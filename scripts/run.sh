
#!/bin/bash

# Move to the project root directory
cd "$(dirname "$0")/.." || exit 1

echo "=========================================="
echo "   OS RESOURCE MANAGEMENT SIMULATOR"
echo "=========================================="

echo "Starting application..."

python src/main.py
