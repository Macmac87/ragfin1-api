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
echo "Adding Dominican Republic data..."
python populate_DO.py
echo "Adding El Salvador data..."
python populate_SV.py
echo "Build complete!"