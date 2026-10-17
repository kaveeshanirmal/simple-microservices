"""API Gateway service configuration — deterministic data for all states."""

SERVICE_ID = "api_gateway"
SERVICE_NAME = "API Gateway"
PORT = 8104

PACKAGES = [
    {"name": "fastapi", "ecosystem": "PyPI", "version": "0.95.0"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Request routed to payment service: /process"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Request routed to catalog service: /products"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "Rate limiter: 142/1000 requests in current window"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "All backend health checks passing"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Request routed to payment service"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "Backend response time elevated: payment at 1800ms"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Circuit breaker half-open for payment backend"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Catalog backend responding normally"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "WARN", "message": "Request queue depth increasing: 45 pending"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "Backend health check failed: payment service unreachable"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Circuit breaker open for payment backend"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "Upstream requests failing, returning 503 to clients"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "Gateway operating in degraded passthrough mode"},
    ],
}

# API Gateway routes to Payment and Catalog.
TRACE_DEFINITIONS = {
    "healthy": [
        {
            "source_id": "api_gateway",
            "target_id": "payment",
            "route": "/process",
            "method": "POST",
            "status_code": 200,
            "duration_ms": 55,
        },
        {
            "source_id": "api_gateway",
            "target_id": "catalog",
            "route": "/products",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 38,
        },
    ],
    "degraded": [
        {
            "source_id": "api_gateway",
            "target_id": "payment",
            "route": "/process",
            "method": "POST",
            "status_code": 503,
            "duration_ms": 1800,
        },
        {
            "source_id": "api_gateway",
            "target_id": "catalog",
            "route": "/products",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 42,
        },
    ],
    "down": [
        {
            "source_id": "api_gateway",
            "target_id": "payment",
            "route": "/process",
            "method": "POST",
            "status_code": 503,
            "duration_ms": 5000,
        },
        {
            "source_id": "api_gateway",
            "target_id": "catalog",
            "route": "/products",
            "method": "GET",
            "status_code": 503,
            "duration_ms": 5000,
        },
    ],
}
