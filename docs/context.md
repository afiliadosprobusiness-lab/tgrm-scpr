# Context

## Project
- Name: Telegram Group/Channel Scraper
- Stack: Python 3.10+, Telethon (MTProto), SQLite, Flask Web UI
- Runtime: Windows, macOS, Linux
- Entry point: `python -m app`

## Architecture
- `app/main.py`: CLI commands (`init-db`, `scrape`, `export`, `stats`, `web`)
- `app/config.py`: env + JSON config loading and validation
- `app/telegram_client.py`: Telethon user-session client and target resolution
- `app/scraper.py`: incremental/backfill scraping, FloodWait handling, retries/backoff
- `app/discovery.py`: source discovery orchestration for non-Telegram connectors (Google Maps and Reddit)
- `app/sources/*`: adapters for Google Maps and Reddit (Telegram uses dedicated scraper workflow)
- `app/sources/capabilities.py`: capability matrix used by API and UI for per-source filter behavior
- `app/storage.py`: SQLite schema and persistence
- `app/exporters.py`: export from SQLite to CSV/JSON
- `app/utils.py`: structured logging, jitter, random sleep, serialization helpers
- `app/web.py`: Flask routes for dashboard, scrape trigger, exports and health
- `app/templates/dashboard.html`: dashboard UI
- `app/static/app.css`: responsive visual styles
- `app/static/dashboard.js`: i18n + theme + platform navigation + filter preview + dynamic capability matrix
  - includes per-source credential override sent as `credentials` in discovery payload
- `api/index.py`: Vercel serverless entrypoint
- `vercel.json`: Vercel routing/build config
- `docs/MANUAL.md`: user-facing operation manual

## Data model
- `targets`:
  - stable `target_id` (Telegram numeric id)
  - `target_username`, `title`, `last_message_id`, `last_scraped_at`
- `messages`:
  - PK `(target_id, message_id)` to avoid duplicates
  - required fields: message metadata, text, entities JSON, optional media metadata
- `scrape_runs`:
  - execution summary and operational metrics
- `source_records`:
  - normalized records from discovery sources (`google_maps`, `reddit`)
- `discovery_runs`:
  - execution summary for discovery filters and results

## Scraping behavior
- Supported targets:
  - public usernames (`@name`)
  - public `t.me` links
  - targets where the logged-in user already has legitimate access
- Not supported:
  - private invite links (`joinchat`, `+hash`)
  - evasion, unauthorized access, spam automation
- Incremental mode:
  - fetch only messages where `message_id > last_message_id`
- Backfill mode:
  - fetch historical messages up to `limit_per_target`
- Safety controls:
  - random pauses between batches/targets
  - retry with exponential backoff
  - FloodWait sleep using Telegram-provided wait + jitter

## Configuration contract
- `.env`:
  - `TELEGRAM_API_ID` (required)
  - `TELEGRAM_API_HASH` (required)
  - `TELEGRAM_SESSION_NAME` (optional)
  - `TELEGRAM_STRING_SESSION` (optional, recommended for serverless/web non-interactive Telegram auth)
  - `GOOGLE_MAPS_API_KEY` (required for Google Maps discovery)
  - `REDDIT_USER_AGENT` (recommended for Reddit discovery requests)
  - `REDDIT_CLIENT_ID` (optional, recommended for Reddit OAuth in serverless)
  - `REDDIT_CLIENT_SECRET` (optional, recommended for Reddit OAuth in serverless)
  - `FLASK_SECRET_KEY` (recommended for web UI)
  - `SCRAPER_DB_PATH` (optional path override)
  - `SCRAPER_CONFIG_PATH` (optional path override)
  - `SCRAPER_ENV_FILE` (optional path override)
  - `SCRAPER_LOG_FILE` (optional path override)
  - `SCRAPER_EXPORTS_PATH` (optional path override)
  - `SCRAPER_MANUAL_PATH` (optional manual file path override)
  - In Vercel runtime, defaults automatically point to `/tmp` for session, DB, logs and exports.
- `config.json`:
  - `targets: string[]`
  - `scrape.limit_per_target: int`
  - `scrape.since_days: int | null`
  - `scrape.sleep_min_ms: int`
  - `scrape.sleep_max_ms: int`
  - `scrape.include_media_metadata: bool`
  - `scrape.batch_size: int`
  - `scrape.max_retries: int`

## Logging and observability
- JSON structured logs at console and `logs/app.log`
- final run summary:
  - targets ok/failed
  - new messages count
  - flood wait occurrences

## Web routes
- `GET /`: dashboard with controls and operational tables.
- `POST /scrape`: executes incremental/backfill/dry-run from UI.
- `POST /api/discover`: executes discovery query for supported non-Telegram sources.
- `GET /api/capabilities`: returns capability matrix per source for UI behavior.
- `POST /export`: exports current DB rows and returns attachment.
- `GET /health`: health probe endpoint.
- `GET /manual`: serves manual file for end users.
- `GET /api/stats`: JSON stats endpoint.

## UX/UI behavior
- Responsive top navbar with source selection:
  - `telegram`
  - `google_maps`
  - `reddit`
- Source-level filter builder:
  - search, niche, has website, has phone, location, rating, verified
- Filter summary preview in UI for selected source.
- Theme switch in dashboard:
  - `light`, `dark`
- Language switch in dashboard:
  - `es`, `en`
- Both preferences persist in browser `localStorage`.
- Layout remains mobile-first and supports desktop grids and overflow-safe tables.
- Active source connectors:
  - `telegram` (scrape workflow)
  - `google_maps` (discovery via Google Places API)
  - `reddit` (discovery via OAuth when configured, with public JSON fallback)
