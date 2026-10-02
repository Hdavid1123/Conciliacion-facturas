# Conciliación de Facturas

Prototipo web para cargar archivos CSV de facturas y contabilidad, ejecutar reglas de conciliación y visualizar un resumen y el detalle de las inconsistencias.

## Alcance

El sistema permite:

* Cargar un archivo de facturas (`facturas.csv`).
* Cargar un archivo de contabilidad (`contabilidad.csv`).
* Validar la estructura de los archivos.
* Ejecutar las reglas de conciliación definidas en `specs/SPEC.md`.
* Clasificar las facturas como `Correcta` o `Con inconsistencia`.
* Mostrar las causas detectadas.
* Mostrar un resumen de resultados.
* Filtrar el detalle por estado.

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
- **`CausaInconsistencia(str, Enum)`:** Serializa directo a JSON como string.
- **Diccionario para duplicados:** Búsqueda O(1) por `id_factura`.
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

- `backend/pyproject.toml`: Python, FastAPI, pytest, etc.
- `backend/uv.lock`: Lockfile del backend.
- `frontend/conciliacion-facturas-ui/package.json`: Angular, Node.js, etc.
- `frontend/conciliacion-facturas-ui/package-lock.json`: Lockfile del frontend.

Para instalar las dependencias:

```bash
cd backend && uv sync
cd frontend/conciliacion-facturas-ui && npm install
```

## Documentación

- [`specs/SPEC.md`](specs/SPEC.md) — Especificación funcional
- [`specs/API.md`](specs/API.md) — Contrato HTTP
- [`specs/TEST-CASES.md`](specs/TEST-CASES.md) — Casos de prueba
- [`backend/README.md`](backend/README.md) — Documentación del backend
- [`frontend/conciliacion-facturas-ui/README.md`](frontend/conciliacion-facturas-ui/README.md) — Documentación del frontend

## Reglas de negocio

Las reglas de negocio implementadas se encuentran en [`specs/SPEC.md`](specs/SPEC.md).

El proceso de desarrollo es incremental:

```text
Especificación
    ↓
Tests
    ↓
Implementación
    ↓
Tests específicos
    ↓
Suite completa
    ↓
Commit
```

## Dependencias

El backend utiliza `uv` y mantiene `uv.lock` versionado.

El frontend utiliza npm y mantiene `package-lock.json` versionado.

No se deben versionar dependencias instaladas localmente como `node_modules` ni entornos virtuales.
