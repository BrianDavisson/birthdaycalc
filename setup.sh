#!/bin/bash
# Setup script for Birthday Age Calculator

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install Flask
pip install --upgrade pip
pip install Flask

echo "\nSetup complete. To run the app:"
echo "source venv/bin/activate && python app.py"
