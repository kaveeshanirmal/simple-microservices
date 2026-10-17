"""Catalog microservice entry point."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.server import create_service_app
from config import SERVICE_ID, SERVICE_NAME, PORT, LOG_ENTRIES, TRACE_DEFINITIONS, PACKAGES

app = create_service_app(
    service_id=SERVICE_ID,
    service_name=SERVICE_NAME,
    port=PORT,
    log_entries=LOG_ENTRIES,
    trace_definitions=TRACE_DEFINITIONS,
    packages=PACKAGES,
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
