#!/bin/bash

# Define the repository URL
REPO_URL="https://github.com/gabi-theo/fastapi_events.git"

# Specify the destination folder (change as needed)
DEST_FOLDER="fastapi_events"

# Clone the repository
git clone "$REPO_URL" "$DEST_FOLDER"

if [ $? -eq 0 ]; then
    echo "Repository cloned successfully into '$DEST_FOLDER'."

    # Create .env file with PostgreSQL configuration
    echo "POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=dev_db" > "$DEST_FOLDER/.env"
    
    echo ".env file generated successfully."
else
    echo "Error: Unable to clone repository."
fi
