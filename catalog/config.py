"""Catalog service configuration — deterministic data for all states."""

SERVICE_ID = "catalog"
SERVICE_NAME = "Catalog"
PORT = 8103

PACKAGES = [
    {"name": "lodash", "ecosystem": "npm", "version": "4.17.20"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Product listing fetched: 42 items"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Cache hit for category electronics"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "Search index query completed in 8ms"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Product detail served for item-7721"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Product listing fetched: 42 items"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "Cache miss rate elevated: 65%"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Database query time above threshold: 450ms"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Fallback to stale cache entry"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "WARN", "message": "Search index replication lag detected"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "Database connection pool exhausted"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Failed to fetch product listing: timeout"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "Search index unavailable"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "All catalog operations halted"},
    ],
}

# Catalog queries the database for product data.
TRACE_DEFINITIONS = {
    "healthy": [
        {
            "source_id": "catalog",
            "target_id": "database",
            "route": "/query",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 6,
        },
    ],
    "degraded": [
        {
            "source_id": "catalog",
            "target_id": "database",
            "route": "/query",
            "method": "GET",
            "status_code": 200,
            "duration_ms": 450,
        },
    ],
    "down": [
        {
            "source_id": "catalog",
            "target_id": "database",
            "route": "/query",
            "method": "GET",
            "status_code": 503,
            "duration_ms": 5000,
        },
    ],
}
