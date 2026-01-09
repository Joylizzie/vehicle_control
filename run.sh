#!/bin/bash

# set -e: Exit on error
# set -u: Exit on unset variables
# set -o pipefail: Pipeline failures trigger exit
set -euo pipefail

# Configuration
export PYTHONPATH=${PYTHONPATH:-}:$(pwd):$(pwd)/src

echo "--- Step 1: Physical Database Creation ---"
python3 src/create_db.py

echo "--- Step 2: Schema and Performance Indexing ---"
python3 src/create_tb_idx.py

echo "--- Step 3: Launching API ---"
# Kill any old process on 8000 so the port is free
fuser -k 8000/tcp > /dev/null 2>&1 || true
# We run this in the background (&) so we can check health in this script
# Or, if you prefer it to block, just run it normally:
uvicorn "src.main:create_app" --factory --host 127.0.0.1 --port 8000 > api.log 2>&1 &

# Store the Process ID of the API
API_PID=$!

# --- Step 4: Health Check Verification ---
echo "Waiting for API health check..."
MAX_RETRIES=5
COUNT=0

while [ $COUNT -lt $MAX_RETRIES ]; do
    # Try to curl the health endpoint
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        echo "✅ API is Healthy and Database is Connected!"
        wait $API_PID
        exit 0
    fi
    echo "Attempt $((COUNT+1)): API not ready yet, retrying in 2s..."
    sleep 2
    COUNT=$((COUNT+1))
done

echo "❌ API failed to reach healthy state."
kill $API_PID
exit 1