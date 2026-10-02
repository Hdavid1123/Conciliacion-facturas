# Conciliación de Facturas

Prototipo web para cargar archivos CSV de facturas y contabilidad, ejecutar reglas de conciliación y visualizar un resumen y el detalle de las inconsistencias.

## Alcance

El sistema permite:

* Cargar `facturas.csv`.
* Cargar `contabilidad.csv`.
* Validar la estructura de los archivos.
* Ejecutar las reglas de conciliación definidas en `specs/SPEC.md`.
* Clasificar las facturas como `Correcta` o `Con inconsistencia`.
* Mostrar las causas detectadas.
* Mostrar un resumen de resultados.
* Filtrar el detalle por estado.

El proyecto no utiliza base de datos, persistencia, autenticación ni infraestructura adicional.

## Arquitectura

El proyecto está dividido en:

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
└── app/
    ├── backend/
    └── frontend/
        └── conciliacion-facturas-ui/
```

## Requisitos

Se requiere tener instalados:

* Git
* Python 3.13+
* uv
* Node.js
* npm
* Angular CLI

Las versiones concretas utilizadas durante el desarrollo deben comprobarse con:

```bash
git --version
python --version
uv --version
node --version
npm --version
ng version
```

## Backend

El backend utiliza Python, FastAPI y `uv` para gestionar el entorno y las dependencias.

Entrar al backend:

```bash
cd app/backend
```

Instalar las dependencias:

```bash
uv sync
```

Ejecutar los tests:

```bash
uv run pytest
```

Iniciar el servidor:

```bash
uv run uvicorn backend.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

La documentación interactiva de FastAPI estará disponible durante el desarrollo en:

```text
http://localhost:8000/docs
```

## Frontend

El frontend utiliza Angular.

Entrar al proyecto:

```bash
cd app/frontend/conciliacion-facturas-ui
```

Instalar las dependencias:

```bash
npm install
```

Iniciar el servidor de desarrollo:

```bash
ng serve
```

La aplicación estará disponible en:

```text
http://localhost:4200
```

## Tests

Los tests del backend deben ejecutarse con:

```bash
cd app/backend
uv run pytest
```

Los tests del frontend pueden ejecutarse con los comandos definidos en `package.json`.

La documentación completa de los tests del backend (estructura, comandos y configuración) se encuentra en [`backend/README.md`](backend/README.md).

## Especificaciones

Las especificaciones funcionales y el contrato de la API se encuentran en:

* `specs/SPEC.md`
* `specs/API.md`
* `specs/TEST-CASES.md`

`AGENTS.md` contiene las reglas de desarrollo que deben respetarse durante la implementación.

## Desarrollo

El proyecto se implementa de forma incremental:

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

Las reglas de negocio no deben inferirse a partir de nombres de campos. Si una especificación es ambigua, debe documentarse la duda antes de implementar una nueva regla.

## Dependencias

El backend utiliza `uv` y mantiene `uv.lock` versionado.

El frontend utiliza npm y mantiene `package-lock.json` versionado.

No se deben versionar dependencias instaladas localmente como `node_modules` ni entornos virtuales.
