"""Database service configuration — deterministic data for all states."""

SERVICE_ID = "database"
SERVICE_NAME = "Database"
PORT = 8105

PACKAGES = [
    {"name": "pg", "ecosystem": "npm", "version": "8.11.3"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Query executed: SELECT in 3ms"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Connection pool: 8/50 active connections"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "WAL checkpoint completed successfully"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Replication lag: 0ms"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Query executed: SELECT in 250ms"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "Connection pool nearing capacity: 42/50"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Slow query detected: full table scan on orders"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "WARN", "message": "Replication lag elevated: 1200ms"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "INFO", "message": "Auto-vacuum triggered on products table"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "Connection pool exhausted, rejecting new connections"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Disk I/O error on primary volume"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "All queries timing out"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "Database process unresponsive, health check failed"},
    ],
}

# Database is a leaf service — no outgoing calls.
TRACE_DEFINITIONS = {
    "healthy": [],
    "degraded": [],
    "down": [],
}
