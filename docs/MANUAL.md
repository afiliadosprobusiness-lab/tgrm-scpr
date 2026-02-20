# Manual de uso - Multi-Source Scraper Panel

## 1) Que es este panel
Este dashboard te permite:
- Elegir una plataforma de origen (Telegram, Google Maps, Instagram, Reddit).
- Definir filtros de busqueda de negocios (nicho, web, telefono, ubicacion, rating).
- Ejecutar scraping real en Telegram.
- Exportar resultados a CSV/JSON.

Importante:
- El backend activo hoy es Telegram.
- Google Maps, Instagram y Reddit estan disponibles en UI como modulos de preparacion (sin scraping backend aun).

## 2) Que debes configurar primero
1. Credenciales en `.env`:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_SESSION_NAME` (opcional)
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
- `Google Maps`, `Instagram`, `Reddit`: modulos en estado "roadmap" (sin extractor backend activo).

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

Nota:
- En esta version, los filtros son de planificacion y construccion de criterio.
- El scraping operativo se ejecuta en el modulo Telegram.

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
- `Color`: Oceano / Ambar / Grafito.
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

## 7) Nota para Vercel
- En serverless, el sistema usa `/tmp` por defecto.
- `/tmp` es efimero: sesion y DB pueden resetearse entre invocaciones.
- Para persistencia real, usa infraestructura con storage persistente.
