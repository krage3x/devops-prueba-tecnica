# Charging Station App

This project is a FastAPI-based application for managing charging stations, charging points, connectors, and their statuses.  

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency and environment management)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)

---

## 1. Install dependencies with Poetry

Poetry is used as the dependency manager for this project.  

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```
## Running the application
### 1. Run locally with Poetry
To run the application locally without Docker, you can use **Gunicorn** with Uvicorn workers.  
Your workdir should be inside **charging_station_app**.
Since dependencies are managed by Poetry, the command must be prefixed with `poetry run`:

```bash
poetry run gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app
```
### 2. Run with Docker Compose

This project uses two environment files located in the `docker/` directory:

- **.db-init.env** → contains the database initialization settings (used when the DB is created for the first time).  
- **.postgres.env** → contains the Postgres credentials and connection settings used by the application.  

Make sure these files are correctly configured before starting the containers.

#### Step 1: Build the Docker image

Before running the containers, build the image from the `Dockerfile`:
```bash
# Run this from the root of the project
docker build -t charging-station-app -f docker/Dockerfile .
```

#### Step 2: Run the docker-compose file
This project uses three environment files located in the `docker/` directory:

- **.db-init.env** → contains the database initialization settings (used when the DB is created for the first time).  
- **.postgres.env** → contains the Postgres credentials to configure the postgres database.
- **.app.env** → contains the Postgres credentials and connection settings used by the application.  

Make sure these files are correctly configured before starting the containers.
Change to the project's docker directory and run:
   ```bash
   cd docker
   source .db-init.env
   source .postres.env
   source .grafana.env
   docker compose up -d
   ```
This will start **four main containers**:

1. **Postgres database (`postgres_db`)**  
   - Stores all your application data.  
   - Exposes port `5432` to the host.

2. **Database initializer (`db_init`)**  
   - Runs only once to initialize the database with schemas, sequences, and initial data.  
   - **Depends on** `postgres_db` to ensure the database is ready before running.

3. **Application (`charging_station_app`)**  
   - Runs the FastAPI application with Gunicorn/Uvicorn.  
   - **Depends on** `db_init` to ensure the database is initialized before the app starts.  
   - Exposes port `8000` to the host: [http://0.0.0.0:8000]

4. **Redis cache (`redis`)**  
   - Used as a cache or for other application state management.  
   - Configured with a **password** for security (set via environment variable).  
   - Exposes port `6379` to the host.  
   - Can start independently but should be ready before the app connects.

 ️ **Dependencies:**  
 - `db_init` depends on `postgres_db`.  
 - `charging_station_app` depends on `db_init` and `redis`.
 ## Notes
 - Only the connectors are cached in Redis. The connector status is not cached because it changes frequently and should always reflect the current state.
 - Make sure the `.env` files in the `docker/` directory are properly configured before starting the containers.
 - When running locally, use Poetry to ensure all dependencies are loaded correctly.