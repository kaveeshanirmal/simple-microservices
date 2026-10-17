"""Reusable Flask application factory for Symphony Demo Microservices.

Each service calls create_service_app() with its own config to get a fully
configured Flask app with /health, /logs, /traces endpoints, 404/500 handlers,
and Content-Type enforcement.
"""

import os
from flask import Flask, jsonify, request


def create_service_app(service_id, service_name, port, log_entries, trace_definitions, packages):
    """Create and configure a Flask app for a demo microservice.

    Args:
        service_id: Stable service identifier (e.g. "auth").
        service_name: Human-readable name (e.g. "Auth").
        port: Port number the service listens on.
        log_entries: Dict keyed by state ("healthy", "degraded", "down"),
                     each value a list of log entry dicts.
        trace_definitions: Dict keyed by state, each value a list of trace
                           request dicts.
        packages: List of package inventory dicts for /inventory.

    Returns:
        Configured Flask application.
    """
    app = Flask(__name__)

    def _get_state():
        """Read the current service state from the environment."""
        state = os.environ.get("SERVICE_STATE", "healthy").lower()
        if state not in ("healthy", "degraded", "down"):
            state = "healthy"
        return state

    def _get_run_id():
        """Extract optional X-Simulation-Run-Id header."""
        return request.headers.get("X-Simulation-Run-Id")

    def _add_run_id(response_dict):
        """Add simulation_run_id to response if header was provided."""
        run_id = _get_run_id()
        if run_id:
            response_dict["simulation_run_id"] = run_id
        return response_dict

    # --- Health endpoint ---

    @app.route("/health", methods=["GET"])
    def health():
        state = _get_state()

        messages = {
            "healthy": f"{service_name} service is operational",
            "degraded": f"{service_name} service is experiencing degraded performance",
            "down": f"{service_name} service is down",
        }

        body = _add_run_id({
            "service_id": service_id,
            "state": state,
            "message": messages[state],
        })

        status_code = 503 if state == "down" else 200
        return jsonify(body), status_code

    # --- Logs endpoint ---

    @app.route("/logs", methods=["GET"])
    def logs():
        state = _get_state()
        entries = log_entries.get(state, [])

        body = _add_run_id({
            "service_id": service_id,
            "entries": entries,
        })

        return jsonify(body), 200

    # --- Traces endpoint ---

    @app.route("/traces", methods=["GET"])
    def traces():
        state = _get_state()
        requests_list = trace_definitions.get(state, [])

        body = _add_run_id({
            "service_id": service_id,
            "requests": requests_list,
        })

        return jsonify(body), 200

    # --- Inventory endpoint ---

    @app.route("/inventory", methods=["GET"])
    def inventory():
        body = _add_run_id({
            "service_id": service_id,
            "packages": packages,
        })

        return jsonify(body), 200

    # --- Error handlers ---

    @app.errorhandler(404)
    def not_found(e):
        body = _add_run_id({
            "error": "not_found",
            "message": "Endpoint not found",
            "service_id": service_id,
        })
        return jsonify(body), 404

    @app.errorhandler(500)
    def internal_error(e):
        body = _add_run_id({
            "error": "internal_error",
            "message": "Simulated internal failure",
            "service_id": service_id,
        })
        return jsonify(body), 500

    # --- Response middleware ---

    @app.after_request
    def set_content_type(response):
        response.headers["Content-Type"] = "application/json"
        return response

    return app
