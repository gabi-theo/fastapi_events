# fastapi_events

## Description

Short fastapi application used for better organisation of events inside buckets


## Prerequisites

- docker
- docker-compose
- python3. >8
## Installation

### Short method
1. Create a new folder
2. Create a bash script and paste the following content:

```
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
```
Please update the destination folder, and postgres variables as needed.
This script will clone the repo, and automatially create .env files. 

To run the application locally, go to cloned folder:

```http
  cd DEST_FOLDER
```
And run:

```http
sh script/run_docker.sh
```

! If you have permission problems running the scripts, what can help is running:
```http
chmod +x script/run_docker.sh
```

The application should be up and running locally, on a docker instance.
Documentation can be read at: 
```http
http://127.0.0.1:8000/docs
```

### Other method
1. Manually clone the public repo from: 
```http
https://github.com/gabi-theo/fastapi_events.git
```
2. Navigate to your cloned folder and create .env file with the following variables:
```
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_SERVER=<url_of_database>
POSTGRES_PORT=<port_of_database>
POSTGRES_DB=<database_name>
```
3.Run:

```http
sh script/run_docker.sh
```

### Running application locally, without docker
In scripts folder there are 3 scripts that can help you running the application locally and populate with mock data if needed:
1. run_server_locally.sh -> will start the application on localhost:8000
2. run_server_locally_with_migrations.sh -> should be used first time, so migrations can be automatially applied
3. run_populate_with_test_data.sh -> will populate db with fake database_name


Unfortunatelly, these 3 scripts have bugs and curently, they don't work and need fixes :(

## Running Tests

To run tests, run the following command

```bash
  sh run_tests.sh
```
