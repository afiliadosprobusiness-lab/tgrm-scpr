# Manual De Uso - Telegram Scraper

## 1) Objetivo
Este sistema extrae mensajes de canales/grupos de Telegram (publicos o accesibles por tu cuenta) y guarda datos en SQLite de forma incremental.

## 2) Requisitos iniciales
1. Configura `.env`:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_SESSION_NAME` (opcional)
2. Configura `config.json`:
   - `targets`
   - parametros de `scrape` (limit, pausas, retries, etc.)

## 3) Flujo recomendado
1. Ejecuta `Dry-run` para validar targets sin scrapear mensajes.
2. Ejecuta scrape incremental para uso diario.
3. Usa backfill solo para historico inicial.
4. Exporta CSV/JSON cuando quieras analizar fuera.

## 4) Opciones de la interfaz web

### Run Scrape
- `Single target (optional)`:
  - Si lo dejas vacio, procesa todos los targets del `config.json`.
  - Si pones un target (`@canal` o `https://t.me/canal`), procesa solo ese.

- `Backfill history`:
  - Descarga historico hacia atras (limitado por `limit_per_target`).
  - Recomendado solo para primera carga.

- `Dry-run only`:
  - Resuelve los targets y muestra `target_id` + `last_message_id`.
  - No guarda mensajes nuevos.
  - Ideal para validar acceso y configuracion.

- `Start Scrape`:
  - Inicia el proceso con las opciones seleccionadas.
  - Al finalizar veras resumen: targets OK/fallidos, mensajes nuevos, flood waits.

### Export Messages
- `Format`:
  - `CSV`: util para Excel/BI.
  - `JSON`: util para pipelines y scripts.
- `Download Export`:
  - Descarga el archivo generado desde la base SQLite.

### Manual rapido + Manual completo
- El dashboard muestra pasos rapidos.
- `Abrir manual completo` descarga/abre este documento.

### Idioma
- Selector `Idioma`:
  - `Español` / `English`
  - Guarda preferencia en el navegador.

### Color
- Selector `Color`:
  - `Oceano`, `Ambar`, `Grafito`
  - Guarda preferencia en el navegador.

## 5) Secciones de monitoreo
- `Configured Targets`: targets definidos en config.
- `Paths`: rutas activas de DB/config/env.
- `Targets Stats`: conteo de mensajes por target y ultimo scrapeo.
- `Recent Runs`: historial de ejecuciones.

## 6) Buenas practicas
- Respeta limites de Telegram (el sistema maneja FloodWait + backoff).
- Evita backfills grandes frecuentes.
- No usar para evadir privados ni spam.

## 7) Notas para Vercel
- En runtime serverless, la app usa `/tmp` para DB/sesion/log/export por defecto.
- `/tmp` es efimero: puede perderse entre invocaciones.
- Para persistencia real, usar infraestructura con storage persistente.

