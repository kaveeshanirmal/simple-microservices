"""Frontend service configuration — deterministic data for all states."""

SERVICE_ID = "frontend"
SERVICE_NAME = "Frontend"
PORT = 8100

PACKAGES = [
    {"name": "react", "ecosystem": "npm", "version": "18.2.0"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Page rendered successfully: /dashboard"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Static assets served: 12 bundles"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "API request proxied to gateway: 200 OK"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "WebSocket connection established for live updates"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Page rendered: /dashboard"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "API gateway response slow: 1200ms"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Partial data loaded, some panels showing stale content"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Fallback UI rendered for unavailable sections"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "WARN", "message": "Retry queued for failed API requests"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "API gateway unreachable: connection refused"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Failed to load dashboard data"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "All upstream requests failing"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "Error boundary activated, displaying fallback page"},
    ],
}

# Frontend calls API Gateway for all backend data.
TRACE_DEFINITIONS = {
    "healthy": [
        {
            "source_id": "frontend",
            "target_id": "api_gateway",
            "route": "/api/v1/request",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 45,
        },
    ],
    "degraded": [
        {
            "source_id": "frontend",
            "target_id": "api_gateway",
            "route": "/api/v1/request",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 1200,
        },
    ],
    "down": [
        {
            "source_id": "frontend",
            "target_id": "api_gateway",
            "route": "/api/v1/request",
            "method": "GET",
            "status_code": 503,
            "duration_ms": 5000,
        },
    ],
}
