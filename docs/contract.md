# Contract

## Scope
This project exposes:
- CLI contract
- Web HTTP contract (Flask dashboard)

## CLI contract

1. `python -m app init-db`
- Effect: creates/updates SQLite schema.
- Exit code: `0` success, non-zero on error.

2. `python -m app scrape [--target TARGET] [--backfill] [--dry-run]`
- Reads env vars: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, optional `TELEGRAM_SESSION_NAME`.
- Reads config from `--config` (default `config.json`).
- `--dry-run`:
  - resolves targets and prints `target_id` + `last_message_id`.
  - does not scrape messages.
- default incremental:
  - stores only messages with `message_id > last_message_id`.
- `--backfill`:
  - fetches older history up to `limit_per_target`.
- Exit code:
  - `0` all targets ok
  - `2` at least one target failed
  - non-zero on fatal errors

3. `python -m app export --format {csv,json} --out PATH`
- Exports all stored rows from `messages` table.
- Creates output directories if missing.

4. `python -m app stats`
- Prints per-target counters and recent scrape runs.

5. `python -m app web [--host HOST] [--port PORT] [--debug]`
- Runs Flask dashboard.
- Default bind: `127.0.0.1:8000`.
- Uses same config/env/DB path arguments (or env overrides).

## Config file contract (`config.json`)
```json
{
  "targets": ["@example", "https://t.me/example"],
  "scrape": {
    "limit_per_target": 2000,
    "since_days": 30,
    "sleep_min_ms": 700,
    "sleep_max_ms": 1600,
    "include_media_metadata": true,
    "batch_size": 200,
    "max_retries": 3
  }
}
```

Validation rules:
- `targets` must be a non-empty list.
- private invite URLs are rejected.
- numeric fields must be > 0 (except sleep values can be 0).
- `sleep_min_ms <= sleep_max_ms`.

## Storage contract (SQLite)
- `targets`:
  - key: `target_id` (Telegram numeric id)
  - `last_message_id` tracks incremental progress
- `messages`:
  - composite PK `(target_id, message_id)`
  - duplicate rows ignored safely
- `scrape_runs`:
  - captures execution summary metrics

## Error contract
- Structured JSON logs at INFO/ERROR level to console and `logs/app.log`.
- Flood wait handling:
  - wait Telegram-provided seconds plus jitter
  - retry without bypassing Telegram limits
- transient RPC/network errors:
  - retry with exponential backoff, bounded by `max_retries`

## Web HTTP contract
1. `GET /`
- Returns HTML dashboard.
- Includes forms for scrape and export plus target/run stats.

2. `POST /scrape`
- Form fields:
  - `target` (optional)
  - `backfill` (optional checkbox)
  - `dry_run` (optional checkbox)
- Executes scrape and persists `scrape_runs`.
- Returns updated dashboard HTML with run summary or error.

3. `POST /export`
- Form field:
  - `format`: `csv` or `json`
- Response: file attachment (`messages_<timestamp>.csv|json`).

4. `GET /health`
- Response JSON:
```json
{"status":"ok"}
```

5. `GET /api/stats`
- Response JSON:
```json
{
  "targets": [],
  "runs": []
}
```

## Environment contract extensions
- `FLASK_SECRET_KEY` (recommended for web session protection)
- `SCRAPER_DB_PATH` (optional DB path override)
- `SCRAPER_CONFIG_PATH` (optional config path override)
- `SCRAPER_ENV_FILE` (optional env file path override)
- `SCRAPER_LOG_FILE` (optional log path override)
- `SCRAPER_EXPORTS_PATH` (optional export path override)
- Runtime default behavior:
  - if `VERCEL` is present, defaults use `/tmp` for DB/log/exports/session.

## Changelog del Contrato
- 2026-02-20
- Cambio: contrato inicial CLI + config + storage.
- Tipo: non-breaking
- Impacto: define interfaz estable para ejecucion y automatizacion local.

- 2026-02-20
- Cambio: agregado contrato web (Flask) y comando CLI `web`.
- Tipo: non-breaking
- Impacto: habilita UI visual y despliegue serverless (Vercel) manteniendo compatibilidad CLI.

- 2026-02-20
- Cambio: fallback automatico a rutas `/tmp` en Vercel para evitar errores de filesystem read-only.
- Tipo: non-breaking
- Impacto: reduce `FUNCTION_INVOCATION_FAILED` por escrituras en rutas no permitidas.
