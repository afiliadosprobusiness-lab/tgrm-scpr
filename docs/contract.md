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

3. `POST /api/discover`
- Request JSON fields:
  - `platform`: `google_maps` | `openstreetmap` | `reddit` | `foursquare` | `yelp` | `tomtom` | `opencorporates`
  - `query`
  - `niche`
  - `has_website`: `any|yes|no`
  - `has_phone`: `any|yes|no`
  - `location`
  - `min_rating`
  - `only_verified`
  - `limit`
  - `credentials` (optional map, e.g. `{ "api_key": "..." }`)
- Response JSON:
  - `status`
  - `source`
  - `count`
  - `items`
  - `recent_runs`
  - `warnings`
  - `applied_filters`
  - `capabilities`
- Persisted in DB:
  - `source_records`
  - `discovery_runs`
  - blocked platforms: `instagram`, `linkedin`

4. `GET /api/capabilities`
- Response JSON:
```json
{
  "platforms": {
    "google_maps": {
      "supports_discovery_api": true,
      "requires_location": false,
      "supports_rating_filter": true,
      "credential_required": true,
      "credential_param": "api_key",
      "configured": false
    }
  }
}
```

5. `POST /export`
- Form field:
  - `format`: `csv` or `json`
- Response: file attachment (`messages_<timestamp>.csv|json`).

6. `GET /health`
- Response JSON:
```json
{"status":"ok"}
```

7. `GET /manual`
- Serves `docs/MANUAL.md` (text/markdown) if available.
- Response: `404` if file does not exist.

8. `GET /api/stats`
- Response JSON:
```json
{
  "targets": [],
  "runs": []
}
```

## Environment contract extensions
- `FLASK_SECRET_KEY` (recommended for web session protection)
- `GOOGLE_MAPS_API_KEY` (required for Google Maps discovery)
- `FOURSQUARE_API_KEY` (required for Foursquare discovery)
- `YELP_API_KEY` (required for Yelp discovery)
- `TOMTOM_API_KEY` (required for TomTom discovery)
- `OPENCORPORATES_API_TOKEN` (required for OpenCorporates discovery)
- `REDDIT_USER_AGENT` (recommended for Reddit discovery)
- `OSM_USER_AGENT` (recommended for OpenStreetMap discovery politeness)
- `SCRAPER_DB_PATH` (optional DB path override)
- `SCRAPER_CONFIG_PATH` (optional config path override)
- `SCRAPER_ENV_FILE` (optional env file path override)
- `SCRAPER_LOG_FILE` (optional log path override)
- `SCRAPER_EXPORTS_PATH` (optional export path override)
- `SCRAPER_MANUAL_PATH` (optional manual file path override)
- Runtime default behavior:
  - if `VERCEL` is present, defaults use `/tmp` for DB/log/exports/session.

## Frontend UI contract
- Dashboard includes:
  - source navbar tabs (`telegram`, `google_maps`, `openstreetmap`, `reddit`, `foursquare`, `yelp`, `tomtom`, `opencorporates`)
  - source filter builder (search, niche, has website, has phone, location, min rating, verified)
  - filter summary preview panel
  - language switch (`es`, `en`)
  - color theme switch (`ocean`, `amber`, `graphite`)
- Preference persistence:
  - browser `localStorage` keys:
    - `dashboard-language`
    - `dashboard-theme`
    - `dashboard-platform`
- Source backend availability:
  - `telegram`: active scrape workflow
  - `google_maps`: active discovery connector (Google Places API)
  - `openstreetmap`: active discovery connector (Nominatim + Overpass)
  - `reddit`: active discovery connector (public JSON)
  - `foursquare`: active discovery connector (Places API)
  - `yelp`: active discovery connector (Fusion API)
  - `tomtom`: active discovery connector (Search API)
  - `opencorporates`: active discovery connector (company registry API)
  - `instagram` / `linkedin`: intentionally disabled from active UI due policy/compliance risk

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

- 2026-02-20
- Cambio: agregado endpoint `/manual` y contrato UI para switches de idioma/color.
- Tipo: non-breaking
- Impacto: mejora usabilidad del dashboard y soporte bilingue.

- 2026-02-20
- Cambio: agregado navbar por fuente y filtro multi-criterio de negocios en la UI.
- Tipo: non-breaking
- Impacto: prepara extension multi-fuente sin romper scraping Telegram existente.

- 2026-02-20
- Cambio: activados conectores discovery para Google Maps y Reddit; Instagram removido por riesgo de cumplimiento.
- Tipo: non-breaking
- Impacto: habilita busqueda real multi-fuente en /api/discover manteniendo Telegram scrape estable.

- 2026-02-20
- Cambio: agregados conectores discovery para OpenStreetMap, Foursquare, Yelp, TomTom y OpenCorporates; LinkedIn bloqueado por cumplimiento.
- Tipo: non-breaking
- Impacto: expande cobertura de fuentes seguras con APIs oficiales/publicas y mantiene bloqueo de plataformas con alto riesgo de restricciones.

- 2026-02-20
- Cambio: agregada matriz de capacidades por fuente + endpoint `GET /api/capabilities`; `POST /api/discover` ahora devuelve `warnings`, `applied_filters` y `capabilities`.
- Tipo: non-breaking
- Impacto: la UI adapta filtros por plataforma y evita ejecuciones ambiguas cuando una fuente no soporta ciertos criterios.
