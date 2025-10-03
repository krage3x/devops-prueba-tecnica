import toml
from fastapi import FastAPI
from app.api import stations,connectors,charging_points
import os


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


@app.get("/")
async def root():
    return {"message": "Welcome to the Charging Station API"}
