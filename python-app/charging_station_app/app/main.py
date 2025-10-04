import toml
from fastapi import FastAPI, Request
from app.api import stations,connectors,charging_points,metrics
from app.api.metrics import REQUEST_LATENCY, REQUEST_COUNT
import time
import os
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,                  # envia logs a stdout
    level=logging.INFO,                 # nivel mínimo a mostrar (INFO, DEBUG, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_version():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pyproject_path = os.path.join(base_path, "pyproject.toml")
    try:
        with open(pyproject_path, "r") as f:
            pyproject = toml.load(f)
            return pyproject["tool"]["poetry"]["version"]
    except Exception:
        return "0.0.0"  # fallback por si falla


app = FastAPI(title="Charging Station API", version=get_version())

# Incluir el router de estaciones
app.include_router(stations.router,  tags=["stations"])
app.include_router(connectors.router,  tags=["connectors"])
app.include_router(charging_points.router,  tags=["charging_points"])
app.include_router(metrics.router,  tags=["metrics"])

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    elapsed = time.time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(elapsed)
    # Increase counter for every petition for each endpoint
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to the Charging Station API"}
