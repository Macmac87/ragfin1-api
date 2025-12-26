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
echo "Populating database..."
python populate_db_FINAL.py
echo "Adding Guatemala data..."
python populate_GT.py
echo "Build complete!"