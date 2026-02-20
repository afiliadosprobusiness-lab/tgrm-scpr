# Telegram Group/Channel Scraper (Telethon + SQLite + Web UI)

Scraper incremental para grupos/canales de Telegram usando cuenta de usuario (MTProto, no BotFather), con CLI y dashboard web.

## Caracteristicas
- Conexion con `TELEGRAM_API_ID` y `TELEGRAM_API_HASH` desde variables de entorno.
- Targets configurables por `@username` o link `t.me` en `config.json`.
- Scraping incremental por `last_message_id` (no repite mensajes).
- Modo `--backfill` para historico inicial (acotado por target).
- Persistencia en SQLite y export a CSV/JSON.
- Manejo de `FloodWaitError`, reintentos con backoff y pausas aleatorias.
- `--dry-run` para validar targets y ultimo ID sin scrapear.
- Interfaz web para ejecutar scrape/export y ver estadisticas.
- Switch de idioma (ES/EN) y color (Oceano/Ambar/Grafito) en la UI.
- Navbar responsive por fuente (Telegram, Google Maps, OpenStreetMap, Reddit, Foursquare, Yelp, TomTom, OpenCorporates).
- Buscador/filtros por fuente (nicho, web, telefono, ubicacion, rating, verificado).
- Matriz de capacidades por fuente (filtros soportados y ubicacion requerida) aplicada en tiempo real en la UI.
- Campo de credencial por modulo en UI para pasar API key/token/user-agent por solicitud (sin persistir en servidor).
- Manual de uso incluido en `docs/MANUAL.md` y accesible por `/manual`.

## Restricciones de cumplimiento
- Solo canales/grupos publicos o chats donde tu cuenta ya tenga acceso legitimo.
- No se implementa bypass de privados ni funciones de spam.
- Links de invitacion privados (`joinchat`, `+hash`) se rechazan.

## Estructura
```text
telegram-scraper/
  app/
    __init__.py
    __main__.py
    main.py
    config.py
    telegram_client.py
    scraper.py
    storage.py
    exporters.py
    utils.py
    web.py
    templates/dashboard.html
    static/app.css
  api/index.py
  data/
  exports/
  logs/
  docs/
    context.md
    PROJECT_CONTEXT.md
    contract.md
  .env.example
  config.json
  requirements.txt
  vercel.json
  README.md
```

## 1) Obtener API_ID y API_HASH
1. Entra a `https://my.telegram.org` con tu cuenta.
2. Abre `API development tools`.
3. Crea una app y copia `api_id` y `api_hash`.

No uses BotFather para este proyecto.

## 2) Instalacion
```bash
cd telegram-scraper
python -m venv .venv
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Instala dependencias:
```bash
pip install -r requirements.txt
```

Crea `.env` desde el ejemplo:
```bash
cp .env.example .env
```

Edita `.env`:
```env
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_SESSION_NAME=telegram_user_session
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
REDDIT_USER_AGENT=proyectos-sass-scraper/1.0 (by u/your_reddit_user)
OSM_USER_AGENT=proyectos-sass-scraper/1.0 (contact: you@example.com)
FOURSQUARE_API_KEY=your_foursquare_api_key
YELP_API_KEY=your_yelp_api_key
TOMTOM_API_KEY=your_tomtom_api_key
OPENCORPORATES_API_TOKEN=your_opencorporates_api_token
FLASK_SECRET_KEY=change_me_for_web_ui
```

## 3) Configurar targets
Edita `config.json`:
```json
{
  "targets": ["@durov", "https://t.me/telegram"],
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

## 4) Inicializar DB
```bash
python -m app init-db
```

## 5) Iniciar sesion (primera vez)
En la primera ejecucion de scrape, Telethon pedira:
- numero de telefono
- codigo SMS/Telegram
- password 2FA (si aplica)

La sesion se guarda con `TELEGRAM_SESSION_NAME`.

## 6) Uso CLI
Scrape incremental:
```bash
python -m app scrape
```

Solo un target:
```bash
python -m app scrape --target @durov
```

Backfill:
```bash
python -m app scrape --backfill
```

Dry-run:
```bash
python -m app scrape --dry-run
```

Export:
```bash
python -m app export --format csv --out ./exports/messages.csv
python -m app export --format json --out ./exports/messages.json
```

Stats:
```bash
python -m app stats
```

## 7) Uso Web local
Levantar dashboard:
```bash
python -m app web --host 127.0.0.1 --port 8000
```

Abrir:
```text
http://127.0.0.1:8000
```

Desde UI puedes:
- lanzar scrape incremental/backfill/dry-run
- exportar CSV/JSON
- ver stats por target y runs recientes
- cambiar idioma y tema de color
- seleccionar fuente en navbar y definir filtros por fuente
- abrir el manual desde el boton `Abrir manual completo`

Estado de fuentes:
- Telegram: backend activo.
- Google Maps: discovery activo via Google Places API.
- OpenStreetMap: discovery activo via Nominatim + Overpass.
- Reddit: discovery activo via JSON publico.
- Foursquare: discovery activo via Places API oficial.
- Yelp: discovery activo via Fusion API oficial.
- TomTom: discovery activo via Search API oficial.
- OpenCorporates: discovery activo via API oficial de registros mercantiles.
- Instagram y LinkedIn: deshabilitados por restricciones de automatizacion.

Manual:
- Archivo: `docs/MANUAL.md`
- Ruta web: `GET /manual`

## 8) Deploy en Vercel
Este repo ya incluye `vercel.json` y entrypoint `api/index.py`.

Variables recomendadas en Vercel:
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `GOOGLE_MAPS_API_KEY` (si usaras Google Maps)
- `OSM_USER_AGENT` (si usaras OpenStreetMap)
- `REDDIT_USER_AGENT` (si usaras Reddit)
- `FOURSQUARE_API_KEY` (si usaras Foursquare)
- `YELP_API_KEY` (si usaras Yelp)
- `TOMTOM_API_KEY` (si usaras TomTom)
- `OPENCORPORATES_API_TOKEN` (si usaras OpenCorporates)
- `TELEGRAM_SESSION_NAME=/tmp/telegram_user_session`
- `SCRAPER_DB_PATH=/tmp/telegram_scraper.db`
- `SCRAPER_LOG_FILE=/tmp/app.log`
- `SCRAPER_EXPORTS_PATH=/tmp/exports`
- `FLASK_SECRET_KEY=<valor-seguro>`

Deploy:
```bash
npm i -g vercel
vercel
```

Nota de arquitectura serverless:
- En Vercel, `/tmp` es efimero. DB y sesion pueden perderse entre invocaciones.
- Para persistencia real (produccion), usa un host con disco persistente o un backend dedicado.
- La app ya usa `/tmp` por defecto en Vercel para DB/log/export/session si no defines overrides.

## Notas tecnicas
- Paginacion incremental: `iter_messages(..., min_id=last_message_id, reverse=True)`.
- Paginacion backfill: `iter_messages(..., offset_id=cursor_id, reverse=False)`.
- Duplicados evitados por PK compuesta `(target_id, message_id)`.
- No descarga archivos multimedia por defecto, solo metadata opcional.
- Logs estructurados JSON en consola y `logs/app.log`.
