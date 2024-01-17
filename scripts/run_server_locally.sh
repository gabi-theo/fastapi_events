#!/bin/bash

# Load environment variables from .env file
dotenv_path="../.env"
if [ -f "$dotenv_path" ]; then
    source <(dotenv -f "$dotenv_path" export)
else
    echo "Error: .env file not found."
    exit 1
fi

# Start FastAPI server
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
