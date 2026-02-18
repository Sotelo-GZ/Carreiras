# Carreiras Galegas Tracker

Aplicación full-stack para recopilar carreras de `carreirasgalegas.com`, guardarlas en base de datos y mostrarlas en un mapa interactivo con filtros.

## Estructura de carpetas

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── scraper/
│   │   └── services/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── types/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Backend

- FastAPI + SQLAlchemy.
- Scraper con `requests + BeautifulSoup` para extraer nombre, fecha, distancia, tipo, ubicación y URL de origen.
- Normalización en parser (tipo y distancia).
- Geocodificación con Nominatim (OpenStreetMap).
- Job diario con APScheduler.
- API REST:
  - `GET /events`
  - `GET /events?distance=10`
  - `GET /events?type=trail`
  - `GET /events?from=2026-01-01`
  - `GET /events?near=lat,lng&radius=50`
  - Extras: `distanceMin`, `distanceMax`, `page`, `page_size`.

## Frontend

- React + Vite + TypeScript.
- Mapa con Leaflet/OpenStreetMap.
- Marcadores con popup (nombre, fecha, distancia, tipo y enlace).
- Filtros dinámicos sin recarga:
  - fecha desde,
  - tipo,
  - rango de distancia (`distanceMin/distanceMax`),
  - proximidad (`near + radius`) y geolocalización del navegador.
- Lista sincronizada bajo el mapa.
- Paginación simple (50 por página por defecto en API).
- Diseño responsive y minimalista.

## Cómo ejecutar en local

## Guía súper simple (si no tienes experiencia)

Si quieres probarlo **sin tocar código**, sigue estos pasos:

1. Instala Docker Desktop:
   - Windows/Mac: https://www.docker.com/products/docker-desktop/
   - Linux: Docker Engine + Docker Compose plugin.
2. Abre una terminal dentro de esta carpeta del proyecto.
3. Ejecuta:

```bash
make up
```

4. Espera 1-2 minutos la primera vez.
5. Abre en el navegador:
   - Frontend (mapa): `http://localhost:5173`
   - Backend (estado): `http://localhost:8000/health`

Para parar todo:

```bash
make down
```

Para ver logs (si algo falla):

```bash
make logs
```

---

### Comandos rápidos disponibles

```bash
make help
```

Incluye `make up`, `make down`, `make logs`, `make restart` y `make health`.

---

### Opción 1: Docker Compose

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Opción 2: Manual

Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Cómo comprobar que funciona (checklist para principiantes)

1. `http://localhost:8000/health` debe devolver:

```json
{"status":"ok"}
```

2. `http://localhost:8000/events` debe devolver un array JSON (aunque esté vacío si el scraping falla temporalmente).
3. `http://localhost:5173` debe mostrar:
   - título "Próximas carreras en Galicia",
   - mapa,
   - filtros,
   - lista debajo del mapa.
4. Cambia un filtro (por ejemplo tipo `trail`) y verifica que mapa y lista se actualizan sin recargar la página.

## Problemas típicos (y solución rápida)

- **No arranca Docker**: reinicia Docker Desktop y repite `make up`.
- **Puerto ocupado** (`8000` o `5173`): cierra la app que use ese puerto o cambia el mapeo en `docker-compose.yml`.
- **No aparecen eventos**: revisa `make logs`; puede haber cambiado la web origen o fallado geocodificación temporalmente.

## Despliegue

### Backend + DB en Render o Railway

1. Crear servicio web desde carpeta `backend`.
2. Build command: `pip install -r requirements.txt`.
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Variables:
   - `DATABASE_URL` (en producción usar Postgres gestionado por Render/Railway).
   - `GEOCODE_USER_AGENT` opcional.
5. Activar healthcheck con `/health`.

### Frontend en Vercel

1. Importar repo y seleccionar carpeta `frontend`.
2. Build command: `npm run build`.
3. Output dir: `dist`.
4. Variable `VITE_API_BASE_URL` apuntando al backend desplegado.

## Flujo de datos

1. Al arrancar backend, se crea esquema de base de datos y se ejecuta un scraping inicial.
2. El scraper descarga eventos desde la web origen.
3. Se parsean campos, se normalizan distancia/tipo/fecha y se geocodifica ubicación.
4. Se hace upsert en base de datos (`name + date + distance`).
5. APScheduler repite scraping cada 24h.
6. Frontend consulta `GET /events` con filtros activos y renderiza mapa + lista.
7. Si se activa geolocalización, se envía `near=lat,lng` y `radius` para filtrar por proximidad.

## Extras implementados

- Filtro de proximidad con geolocalización del navegador.
- Cache natural por persistencia en base de datos y job diario (evita scraping por petición).

## Mejoras recomendadas para producción avanzada

- Migraciones reales con Alembic.
- Redis para cache de geocoder.
- Reintentos exponenciales para scraper.
- Clustering de marcadores con `react-leaflet-markercluster`.
- Autenticación y favoritos por usuario.
