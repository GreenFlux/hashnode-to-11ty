#!/bin/bash

# Hashnode-to-11ty Reset Script
# Cleans up all generated test files and outputs for a fresh start

echo "🧹 Hashnode-to-11ty Reset Script"
echo "================================="

# Remove all possible output directories
echo "📁 Removing output directories..."
rm -rf test* output* blog* fresh-test simple-test-output 2>/dev/null

# Remove any test files that might have been created
echo "🗑️  Removing test files..."
rm -f test_*.py 2>/dev/null

# Clean Python cache files
echo "🐍 Cleaning Python cache..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Optional: Remove downloaded images (uncomment if desired)
# echo "🖼️  Removing downloaded images..."
# rm -rf images/ 2>/dev/null

echo "✅ Reset complete!"
echo ""
echo "Ready for fresh testing. Try:"
echo "  python h2e.py hashnode-export-example.json --output ./test --limit 2 --dry-run"
echo ""