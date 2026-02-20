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
- `POST /export`
- `GET /health`
- `GET /manual`
- `GET /api/stats`

## UX controls
- Language switch (`es` / `en`) with browser persistence.
- Color/theme switch (`ocean` / `amber` / `graphite`) with browser persistence.
- User manual available in `docs/MANUAL.md` and route `/manual`.

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
