# Manual de uso - Multi-Source Scraper Panel

## 1) Que es este panel
Este dashboard te permite:
- Elegir una plataforma de origen (Telegram, Google Maps, Reddit).
- Definir filtros de busqueda de negocios (nicho, web, telefono, ubicacion, rating).
- Ejecutar scraping real en Telegram y discovery real en todas las fuentes no-Telegram.
- Exportar resultados a CSV/JSON.

Importante:
- Telegram mantiene su flujo de scraping incremental.
- Google Maps y Reddit usan discovery activo via APIs oficiales/publicas.

## 2) Que debes configurar primero
1. Credenciales en `.env`:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_SESSION_NAME` (opcional)
   - `TELEGRAM_STRING_SESSION` (recomendado en Vercel/web para evitar login interactivo)
   - `GOOGLE_MAPS_API_KEY` (para Google Maps)
   - `REDDIT_USER_AGENT` (recomendado para Reddit)
   - `REDDIT_CLIENT_ID` y `REDDIT_CLIENT_SECRET` (recomendado en Vercel para OAuth oficial)
2. Targets en `config.json`:
   - `targets`: `@canal` o `https://t.me/canal`
   - `scrape`: limites, pausas, retries.

## 3) Flujo recomendado (paso a paso)
1. Abre el dashboard.
2. En el navbar, selecciona `Telegram`.
3. Usa el bloque `Source Search and Filters` para definir tu criterio.
4. Ejecuta `Dry-run` primero para validar acceso.
5. Ejecuta scrape incremental (sin backfill) para operacion diaria.
6. Usa backfill solo para historico inicial.
7. Exporta CSV/JSON para analisis externo.

## 4) Explicacion de cada opcion

### A) Navbar de plataformas
- `Telegram`: modulo activo para scraping real.
- `Google Maps`: modulo activo para discovery.
- `Reddit`: modulo activo para discovery.

### B) Source Search and Filters
- `Search`: palabra clave o consulta base.
- `Business niche`: categoria del negocio.
- `Has website`: filtra por presencia de sitio web.
- `Has phone`: filtra por presencia de telefono.
- `Location`: ciudad/pais objetivo.
- `Minimum rating`: umbral de calidad.
- `Only verified profiles`: prioriza perfiles verificados.
- `Apply Filters`: guarda y muestra resumen de filtros activos.
- `Reset`: limpia filtros.
- `Capabilities`: el panel muestra una matriz por fuente (si requiere ubicacion y que filtros soporta).
- `Module credential`: campo para pegar API key/token/user-agent por fuente sin tocar `.env`.

Nota:
- En Telegram, los filtros te ayudan a definir criterio, y la ejecucion real va por bloque `Run Scrape`.
- En fuentes no Telegram, `Apply Filters` ejecuta discovery real y devuelve resultados en tabla.
- Si un filtro no aplica a la fuente, se desactiva automaticamente en la UI.
- Si una fuente requiere credencial y no esta en servidor, puedes pegarla en `Module credential`.

### C) Run Scrape (Telegram)
- `Single target (optional)`:
  - Vacio = procesa todos los targets del `config.json`.
  - Con valor = procesa solo ese target.
- `Backfill history`:
  - Descarga historico hacia atras hasta el limite configurado.
- `Dry-run only`:
  - Resuelve target IDs y muestra estado sin guardar mensajes.
- `Start scrape`:
  - Ejecuta el scraping con las opciones marcadas.

### D) Export Messages
- `Format`:
  - `CSV`: Excel/BI.
  - `JSON`: pipelines/script.
- `Download export`:
  - Descarga los mensajes almacenados en SQLite.

### E) Preferencias UI
- `Idioma`: Espanol / English.
- `Color`: Claro / Oscuro.
- Ambas opciones se guardan en el navegador.

## 5) Bloques informativos
- `Configured Targets`: targets cargados desde config.
- `Paths`: rutas activas de DB/config/env.
- `Targets Stats`: volumen por target y ultimo scrapeo.
- `Recent Runs`: historial de corridas.

## 6) Buenas practicas
- Ejecuta siempre `Dry-run` antes del primer scrape real.
- Evita backfills muy grandes en horarios cortos.
- Respeta FloodWait y limites de plataforma.
- No intentes acceso no autorizado ni automatizacion de spam.

## 8) Matriz rapida de capacidades por fuente
- Google Maps: rating `si`, verificado `si`, web `si`, telefono `si`, ubicacion requerida `no`.
- Reddit: rating `no`, verificado `si`, web `si`, telefono `si`, ubicacion requerida `no`.
  Usa OAuth oficial si defines `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET`.

## 9) Nota para Vercel
- En serverless, el sistema usa `/tmp` por defecto.
- `/tmp` es efimero: sesion y DB pueden resetearse entre invocaciones.
- Para persistencia real, usa infraestructura con storage persistente.
- El scraping Telegram via web no puede pedir codigo SMS; configura `TELEGRAM_STRING_SESSION`.
