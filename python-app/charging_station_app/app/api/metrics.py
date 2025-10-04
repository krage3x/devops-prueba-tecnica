from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Metrics for connectors
CONNECTORS_CREATED = Counter(
    "connectors_created_total",
    "Total connectors created"
)
CONNECTORS_DELETED = Counter(
    "connectors_deleted_total",
    "Total connectors deleted"
)
CONNECTORS_UPDATED = Counter(
    "connectors_updated_total",
    "Total connectors updated"
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

# Histogram for latency
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.05, 0.1, 0.3, 0.5, 1, 2, 5]
)
router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}}
)

#Prometheus endpoint for metrics
@router.get("/")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
