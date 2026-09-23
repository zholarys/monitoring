# DevOps Lab — Monitoring & Logging from Scratch

A Docker Compose stack demonstrating monitoring and centralized logging built from the ground up, without relying on managed or pre-built solutions.

## Architecture

- **Metrics**: Prometheus + node-exporter (host metrics) + blackbox-exporter (health checks)
- **Logs**: Loki + Grafana Alloy (log collection via Docker socket, auto-labeled by service)
- **Visualization**: Grafana — unified dashboard with metrics and logs side by side
- **Alerting**: Alertmanager
- **Application layer**: Nginx, FastAPI backend, PostgreSQL, Redis

## What it shows

- Setting up Prometheus scraping and Grafana dashboards from zero
- Centralized log collection across all containers using Loki + Alloy, with retention policy (7 days)
- A single dashboard combining CPU/RAM/disk metrics, endpoint health checks, response time, live logs per service, log volume by service, and cross-service error filtering
- Diagnosing and fixing a real permission issue during Loki's first startup (volume ownership mismatch between the container's non-root UID and the host-created volume)

## Stack

Docker Compose, Prometheus, Grafana, Loki, Grafana Alloy, Alertmanager, Nginx, FastAPI, PostgreSQL, Redis

## Usage

\`\`\`bash
docker compose up -d
\`\`\`

Grafana is available at \`http://localhost:3000\`. The \`DevopsLab\` dashboard includes a \`\$service\` variable for switching between containers' logs.
