#!/bin/bash

dotenv_path="./.env"

if [ -f "$dotenv_path" ]; then
    # Load environment variables from .env file
    . "$dotenv_path"
    DATABASE_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:$POSTGRES_PORT/$POSTGRES_DB"
    echo "DATABASE_URL: $DATABASE_URL"
else
    echo "Error: .env file not found."
    exit 1
fi

ALEMBIC_INI_PATH="alembic.ini"
SQLALCHEMY_URL_LINE="sqlalchemy.url = $DATABASE_URL"

# Initialize alembic if it doesn't exist
if [ ! -d "alembic" ]; then
    alembic init alembic
    sed -i "s|^sqlalchemy.url.*|$SQLALCHEMY_URL_LINE|" "$ALEMBIC_INI_PATH"
fi

# Run migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head

echo "Migrations completed successfully!"