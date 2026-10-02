# Conciliación de Facturas

Prototipo web para cargar archivos CSV de facturas y contabilidad, ejecutar reglas de conciliación y visualizar un resumen y el detalle de las inconsistencias.

## Alcance

El sistema permite:

- Cargar un archivo de facturas (`facturas.csv`).
- Cargar un archivo de contabilidad (`contabilidad.csv`).
- Validar la estructura de los archivos.
- Ejecutar las reglas de conciliación definidas en `specs/SPEC.md`.
- Clasificar las facturas como `Correcta` o `Con inconsistencia`.
- Mostrar las causas detectadas.
- Mostrar un resumen de resultados.
- Filtrar el detalle por estado.

El proyecto no utiliza base de datos, persistencia, autenticación ni infraestructura adicional.

## Arquitectura

```text
CSV
 ↓
Validación y parseo
 ↓
Servicio de conciliación
 ↓
Reglas de negocio
 ↓
Resultado
 ↓
FastAPI
 ↓
Angular
```

El backend contiene la lógica de conciliación independientemente de FastAPI para que pueda probarse sin iniciar el servidor.

## Decisiones de diseño

### Backend

- **Conciliación independiente de FastAPI:** Permite probar la lógica sin levantar el servidor.
- **`Decimal` para valores monetarios:** Evita errores de punto flotante.
- **`date | None` para fechas:** Permite identificar facturas con fechas inválidas sin rechazar el archivo.
- **`id_factura_linea`:** Permite distinguir registros duplicados por posición.

### Proyecto

- **Sin base de datos ni persistencia:** SPEC.md no lo requiere.
- **Un solo endpoint:** API.md solo define `POST /api/conciliacion`.
- **`uv` para dependencias:** Gestiona entorno virtual y lockfile.

## Estructura

```text
.
├── AGENTS.md
├── MEMORY.md
├── README.md
├── specs/
│   ├── SPEC.md
│   ├── API.md
│   └── TEST-CASES.md
├── backend/
│   ├── src/backend/
│   │   ├── main.py
│   │   ├── api/
│   │   └── conciliacion/
│   ├── tests/
│   └── README.md
└── frontend/
    └── conciliacion-facturas-ui/
        └── README.md
```

## Versiones

Las versiones de dependencias se gestionan automáticamente:

- `backend/pyproject.toml`: Python >= 3.13, FastAPI >= 0.142.2, python-multipart >= 0.0.32, uvicorn >= 0.54.0.
- `backend/uv.lock`: Lockfile del backend.
- `frontend/conciliacion-facturas-ui/package.json`: Angular ^22.2.0, Angular CLI ^22.2.0, TypeScript ~6.0.2, Vitest ^5.0.0, npm@11.12.1.
- `frontend/conciliacion-facturas-ui/package-lock.json`: Lockfile del frontend.

Para instalar las dependencias:

```bash
cd backend && uv sync
cd frontend/conciliacion-facturas-ui && npm install
```

## Pruebas y datos de ejemplo

Los archivos de ejemplo se encuentran en `raw_data/`:

- `raw_data/facturas.csv`: Archivo de facturas con casos de prueba.
- `raw_data/contabilidad.csv`: Archivo de contabilidad con casos de prueba.

Los tests automatizados se encuentran en:

- `backend/tests/`: Tests del backend (40 tests).
- `frontend/conciliacion-facturas-ui/src/app/`: Tests del frontend (8 tests).

Los tests utilizan data modificada internamente en base a los archivos iniciales de `raw_data/`. Cada test crea sus propios datos de entrada en el código para validar casos específicos sin modificar los archivos originales.

Para ejecutar los tests del backend:

```bash
cd backend
uv run python -m pytest
```

Para ejecutar los tests del frontend:

```bash
cd frontend/conciliacion-facturas-ui
ng test
```

## Documentación

- [`specs/SPEC.md`](specs/SPEC.md) — Especificación funcional
- [`specs/API.md`](specs/API.md) — Contrato HTTP
- [`specs/TEST-CASES.md`](specs/TEST-CASES.md) — Casos de prueba
- [`backend/README.md`](backend/README.md) — Documentación del backend
- [`frontend/conciliacion-facturas-ui/README.md`](frontend/conciliacion-facturas-ui/README.md) — Documentación del frontend

## Reglas de negocio

Las reglas de negocio implementadas se encuentran en [`specs/SPEC.md`](specs/SPEC.md).

El proceso de desarrollo es incremental.

## Dependencias

El backend utiliza `uv` y mantiene `uv.lock` versionado.

El frontend utiliza npm y mantiene `package-lock.json` versionado.