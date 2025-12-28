#!/usr/bin/env bash
set -o errexit
echo "Installing frontend dependencies..."
cd frontend
npm install
echo "Building frontend..."
npm run build
cd ..
echo "Installing backend dependencies..."
pip install -r requirements.txt
echo "Populating database with all countries and providers..."
python populate_db_FINAL.py
echo "Build complete!"