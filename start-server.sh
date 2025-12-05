#!/bin/bash
# Simple script to start a local web server for previewing sections

echo "Starting local web server..."
echo "Open http://localhost:8000/sections/overview.html in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

# Try Python 3 first, then Python 2, then PHP
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer 8000
elif command -v php &> /dev/null; then
    php -S localhost:8000
else
    echo "Error: No web server found. Please install Python or PHP."
    exit 1
fi

