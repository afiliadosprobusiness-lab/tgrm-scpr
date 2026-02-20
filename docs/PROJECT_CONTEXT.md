# PROJECT_CONTEXT

Operational summary for the Telegram scraper.

## Commands
- `python -m app init-db`
- `python -m app scrape`
- `python -m app scrape --target @name`
- `python -m app scrape --backfill`
- `python -m app scrape --dry-run`
- `python -m app export --format csv --out ./exports/messages.csv`
- `python -m app export --format json --out ./exports/messages.json`
- `python -m app stats`
- `python -m app web --host 127.0.0.1 --port 8000`

## Web routes
- `GET /`
- `POST /scrape`
- `POST /api/discover`
- `GET /api/capabilities`
- `POST /export`
- `GET /health`
- `GET /manual`
- `GET /api/stats`

## UX controls
- Language switch (`es` / `en`) with browser persistence.
- Color/theme switch (`ocean` / `amber` / `graphite`) with browser persistence.
- Source navbar (`telegram`, `google_maps`, `openstreetmap`, `reddit`, `foursquare`, `yelp`, `tomtom`, `opencorporates`) with responsive menu.
- Source filter builder (search, niche, website, phone, location, rating, verified).
- Dynamic source capability matrix (filter availability + required location) from backend.
- Per-module credential override in UI (key/token/user-agent) for discovery requests.
- On-screen filter preview for the currently selected source.
- User manual available in `docs/MANUAL.md` and route `/manual`.

## Source status
- Telegram: active backend scraping module.
- Google Maps: active discovery connector (Google Places API).
- OpenStreetMap: active discovery connector (Nominatim + Overpass).
- Reddit: active discovery connector (public JSON).
- Foursquare: active discovery connector (Places API).
- Yelp: active discovery connector (Fusion API).
- TomTom: active discovery connector (Search API).
- OpenCorporates: active discovery connector (company registry API).
- Instagram/LinkedIn: intentionally disabled due policy/compliance risk for automated scraping.

## Incremental state
- last processed id is persisted per target in SQLite (`targets.last_message_id`).
- incremental mode only requests messages newer than that id.

## Compliance
- Only public targets or chats with legitimate access by the user account.
- No private invite bypassing, no spam automation, no member scraping by default.

## Output paths
- DB: `data/telegram_scraper.db`
- Logs: `logs/app.log`
- Exports: `exports/`

## Vercel notes
- Includes `vercel.json` + `api/index.py`.
- For serverless runtime, prefer env path overrides to `/tmp`:
  - `SCRAPER_DB_PATH=/tmp/telegram_scraper.db`
  - `TELEGRAM_SESSION_NAME=/tmp/telegram_user_session`
- App default already falls back to `/tmp` in Vercel when those vars are not set.
