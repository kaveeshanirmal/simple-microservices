"""Payment service configuration — deterministic data for all states.

The payment → auth trace is the critical hidden dependency that Symphony's
investigator agent must discover through trace evidence.
"""

SERVICE_ID = "payment"
SERVICE_NAME = "Payment"
PORT = 8102

PACKAGES = [
    {"name": "jinja2", "ecosystem": "PyPI", "version": "2.4.1"},
]

LOG_ENTRIES = {
    "healthy": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Transaction processed: order-1001"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "INFO", "message": "Token validated via auth service"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "INFO", "message": "Payment confirmation sent to gateway"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Ledger entry recorded successfully"},
    ],
    "degraded": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "INFO", "message": "Transaction processing started: order-1001"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "WARN", "message": "Auth token validation slow: 2500ms"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "WARN", "message": "Upstream auth service returned 429, retrying"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "INFO", "message": "Retry succeeded, token validated"},
        {"timestamp": "2026-01-15T10:00:04Z", "level": "WARN", "message": "Transaction latency above SLA threshold"},
    ],
    "down": [
        {"timestamp": "2026-01-15T10:00:00Z", "level": "ERROR", "message": "Auth service unreachable: connection timeout after 5000ms"},
        {"timestamp": "2026-01-15T10:00:01Z", "level": "ERROR", "message": "Token validation failed: auth service returned 503"},
        {"timestamp": "2026-01-15T10:00:02Z", "level": "ERROR", "message": "Cannot process transaction without valid token"},
        {"timestamp": "2026-01-15T10:00:03Z", "level": "ERROR", "message": "All payment operations halted: dependency failure"},
    ],
}

# Payment calls auth to validate tokens (hidden dependency) and database for transactions.
TRACE_DEFINITIONS = {
    "healthy": [
        {
            "source_id": "payment",
            "target_id": "auth",
            "route": "/validate-token",
            "method": "POST",
            "status_code": 200,
            "duration_ms": 12,
        },
        {
            "source_id": "payment",
            "target_id": "database",
            "route": "/transactions",
            "method": "POST",
            "status_code": 200,
            "duration_ms": 8,
        },
    ],
    "degraded": [
        {
            "source_id": "payment",
            "target_id": "auth",
            "route": "/validate-token",
            "method": "POST",
            "status_code": 429,
            "duration_ms": 2500,
        },
        {
            "source_id": "payment",
            "target_id": "database",
            "route": "/transactions",
            "method": "POST",
            "status_code": 200,
            "duration_ms": 350,
        },
    ],
    "down": [
        {
            "source_id": "payment",
            "target_id": "auth",
            "route": "/validate-token",
            "method": "POST",
            "status_code": 503,
            "duration_ms": 5000,
        },
        {
            "source_id": "payment",
            "target_id": "database",
            "route": "/transactions",
            "method": "POST",
            "status_code": 503,
            "duration_ms": 5000,
        },
    ],
}
