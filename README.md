# POAI Phase 3 — Hosted Screenshot Analysis (FastAPI + PostgreSQL)

A deployable foundation to host the POAI dashboard/API without XAMPP. Desktop capture is a separate sender client because a cloud host cannot capture a screenshot from your personal Pocket Option desktop. OTC and STANDARD context are stored separately.

## Local or VPS launch (Docker)
1. Install Docker Desktop (Windows) or Docker Engine + Compose (Linux VPS).
2. Copy `.env.example` to `.env`; generate strong secrets for `POSTGRES_PASSWORD` and `API_KEY`. Keep `.env` private.
3. Run `docker compose up -d --build`.
4. Verify `http://127.0.0.1:8000/health`; open dashboard `http://127.0.0.1:8000`; API docs `/docs`.
5. Enter `API_KEY` into dashboard. Upload a chart screenshot to test.

## Hosting publicly
Deploy on a VPS with Docker. Put a reverse proxy (Caddy/Nginx) in front with HTTPS; do not expose PostgreSQL. Configure firewall for 80/443 only, keep API behind HTTPS. Current Compose binds app to localhost intentionally. Configure proxy to 127.0.0.1:8000. Rotate secrets before public deployment, enable backups, monitor disk use, and apply rate limiting. This starter has API-key access but no user account/roles yet.

## Desktop screenshot client
On Windows PC that displays the chart: `python -m venv .venv`, activate, `pip install -r requirements.txt`. Then:
`python client/screenshot_sender.py --api https://YOUR_DOMAIN/api/analyze --key YOUR_API_KEY --asset EURUSD --market OTC --timeframe M1 --interval 5`
The sender currently captures the chosen monitor full-screen. Use monitor selection or crop customization before continuous use to avoid including unrelated content. `--once` runs a single capture.

## Analysis limitation
The present analyzer is a conservative OpenCV visual heuristic—not a trained candle model and not reliable price extraction. It labels color imbalance, caps confidence, and uses no authoritative broker prices. Entry zone is explicitly an estimate. For professional-grade predictive performance, use labeled screenshots split by asset, OTC/standard, timeframe, and outcome; train/validate with out-of-sample chronological testing, calibration, and leakage prevention. Never use signals as guaranteed trades. No broker execution is included.

## Routes
- `GET /health` health check
- `GET /api/signals` (API key) signal journal
- `POST /api/signals` (API key) ingest reviewed signal JSON
- `POST /api/analyze` (API key) screenshot upload and heuristic
- `/docs` interactive API schema

## Backups
`docker compose exec -T db pg_dump -U poai poai > poai_backup.sql`
