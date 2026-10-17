"""Auth service configuration — deterministic data for all states."""

SERVICE_ID = "auth"
SERVICE_NAME = "Auth"
PORT = 8101

PACKAGES = [
    {"name": "pyjwt", "ecosystem": "PyPI", "version": "1.7.1"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Token validation completed"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Session refreshed for user-42"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "JWT signature verified successfully"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Access token issued, expires in 3600s"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Token validation completed"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "Token validation latency elevated: 850ms"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Session store response time above threshold"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Retry succeeded for session lookup"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "WARN", "message": "Connection pool nearing capacity: 45/50"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "Failed to connect to session store: connection refused"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Token validation failed: internal error"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "Health check failed: unable to reach backing store"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "All retry attempts exhausted, service unavailable"},
    ],
}

# Auth is a leaf service — no outgoing calls to other services.
TRACE_DEFINITIONS = {
    "healthy": [],
    "degraded": [],
    "down": [],
}
