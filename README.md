# Symphony Demo Microservices

Standalone Docker Compose project containing six HTTP microservices for the Symphony application. These services provide real `/health`, `/logs`, `/traces`, and `/inventory` endpoints that Symphony can query through its adapter layer.

**This project is completely independent of Symphony.** It shares no code, no imports, and no environment variables with the Symphony Jac application.

## Required Tools

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+, included with Docker Desktop)

## Quick Start

```bash
# Start all services
docker compose up --build

# Start in background
docker compose up --build -d

# Stop all services
docker compose down
```

## Services

| Service | URL | Port | Service ID |
| --- | --- | --- | --- |
| Frontend | http://localhost:8100 | 8100 | `frontend` |
| Auth | http://localhost:8101 | 8101 | `auth` |
| Payment | http://localhost:8102 | 8102 | `payment` |
| Catalog | http://localhost:8103 | 8103 | `catalog` |
| API Gateway | http://localhost:8104 | 8104 | `api_gateway` |
| Database | http://localhost:8105 | 8105 | `database` |

## Dependency Topology

```
Frontend → API Gateway → Payment → Database
                      ↘ Catalog  → Database
           Payment → Auth (hidden — discovered via traces)
```

## Endpoints

All endpoints return `Content-Type: application/json`.

### GET /health

```bash
curl http://localhost:8101/health
```

```json
{
  "service_id": "auth",
  "state": "healthy",
  "message": "Auth service is operational"
}
```

### GET /logs

```bash
curl http://localhost:8101/logs
```

```json
{
  "service_id": "auth",
  "entries": [
    {
      "timestamp": "2026-01-15T10:00:00Z",
      "level": "INFO",
      "message": "Token validation completed"
    }
  ]
}
```

### GET /traces

```bash
curl http://localhost:8102/traces
```

```json
{
  "service_id": "payment",
  "requests": [
    {
      "source_id": "payment",
      "target_id": "auth",
      "route": "/validate-token",
      "method": "POST",
      "status_code": 200,
      "duration_ms": 12
    }
  ]
}
```

### GET /inventory

```bash
curl http://localhost:8103/inventory
```

```json
{
  "service_id": "catalog",
  "packages": [
    {
      "name": "lodash",
      "ecosystem": "npm",
      "version": "4.17.20"
    }
  ]
}
```

### Error Responses

Unknown endpoints return HTTP 404:

```bash
curl http://localhost:8101/nonexistent
```

```json
{
  "error": "not_found",
  "message": "Endpoint not found",
  "service_id": "auth"
}
```

## Failure Simulation

Each service's state is controlled by environment variables:

| Variable | Controls | Values |
| --- | --- | --- |
| `FRONTEND_STATE` | Frontend | `healthy` (default), `degraded`, `down` |
| `AUTH_STATE` | Auth | `healthy` (default), `degraded`, `down` |
| `PAYMENT_STATE` | Payment | `healthy` (default), `degraded`, `down` |
| `CATALOG_STATE` | Catalog | `healthy` (default), `degraded`, `down` |
| `API_GATEWAY_STATE` | API Gateway | `healthy` (default), `degraded`, `down` |
| `DATABASE_STATE` | Database | `healthy` (default), `degraded`, `down` |

### Scenario Examples

```bash
# Normal operation — all services healthy
docker compose up --build

# Auth outage — auth is down, cascading impact visible in traces
AUTH_STATE=down PAYMENT_STATE=degraded API_GATEWAY_STATE=degraded FRONTEND_STATE=degraded docker compose up --build

# Payment outage
PAYMENT_STATE=down API_GATEWAY_STATE=degraded FRONTEND_STATE=degraded docker compose up --build

# Database failure — affects payment and catalog
DATABASE_STATE=down PAYMENT_STATE=degraded CATALOG_STATE=degraded docker compose up --build

# Single service down
AUTH_STATE=down docker compose up --build

# Everything down
FRONTEND_STATE=down AUTH_STATE=down PAYMENT_STATE=down CATALOG_STATE=down API_GATEWAY_STATE=down DATABASE_STATE=down docker compose up --build
```

When `SERVICE_STATE=down`:
- `/health` returns HTTP 503 with `"state": "down"`
- `/logs` returns ERROR-level entries showing failure symptoms
- `/traces` returns failed/timed-out trace entries (where applicable)

## Optional Header

All endpoints accept an optional correlation header:

```bash
curl -H "X-Simulation-Run-Id: run-42" http://localhost:8101/health
```

When provided, the response includes `"simulation_run_id": "run-42"`. This header is for correlation only — the services never depend on it for behavior.

## Integration with Symphony

Symphony's adapter should:

1. Call `GET http://localhost:{port}/{endpoint}` for each service
2. Optionally send `X-Simulation-Run-Id` header for correlation
3. Convert the JSON responses into Symphony's `Evidence` records

The microservices know nothing about Jac, Evidence records, OperationEnvelopes, or Symphony's internal state. The integration boundary is HTTP + JSON only.

## Project Structure

```
microservices/
├── docker-compose.yml
├── README.md
├── shared/
│   ├── server.py               # Reusable Flask app factory
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── Dockerfile
│   ├── main.py
│   └── config.py               # Traces: frontend → api_gateway
├── auth/
│   ├── Dockerfile
│   ├── main.py
│   └── config.py               # Leaf service, no outgoing traces
├── payment/
│   ├── Dockerfile
│   ├── main.py
│   └── config.py               # Traces: payment → auth (hidden!) + database
├── catalog/
│   ├── Dockerfile
│   ├── main.py
│   └── config.py               # Traces: catalog → database
├── api_gateway/
│   ├── Dockerfile
│   ├── main.py
│   └── config.py               # Traces: api_gateway → payment + catalog
└── database/
    ├── Dockerfile
    ├── main.py
    └── config.py               # Leaf service, no outgoing traces
```
