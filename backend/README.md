# Backend — Conciliador de Facturas

## Ejecución

```bash
uv run python -m uvicorn backend.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

La documentación interactiva de FastAPI estará disponible en `http://localhost:8000/docs`.

## Tests

### Ejecutar todos los tests

```bash
uv run python -m pytest
```

### Ejecutar un archivo específico

```bash
uv run python -m pytest tests/test_reglas.py
uv run python -m pytest tests/test_csv_parser.py
uv run python -m pytest tests/test_service.py
uv run python -m pytest tests/test_api.py
```

### Ejecutar un test específico

```bash
uv run python -m pytest tests/test_reglas.py::test_r1_iva_correcto
```

### Con output detallado

```bash
uv run python -m pytest -v
```

## Estructura de tests

| Archivo | Tests | Cobertura |
|---|---|---|
| `tests/test_reglas.py` | 20 | R1–R9 (reglas de negocio) |
| `tests/test_csv_parser.py` | 10 | Parseo y validación de CSV |
| `tests/test_service.py` | 5 | Orquestación y resumen |
| `tests/test_api.py` | 5 | Integración e2e |

## Estructura del backend

```text
backend/
├── src/backend/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── api/
│   │   └── router.py        # POST /api/conciliacion
│   └── conciliacion/
│       ├── modelos.py       # Dataclasses y enums
│       ├── csv_parser.py    # Parseo y validación de CSV
│       ├── reglas.py        # R1–R9 (reglas de negocio)
│       └── service.py       # Orquestación
└── tests/
    ├── test_reglas.py
    ├── test_csv_parser.py
    ├── test_service.py
    └── test_api.py
```

## Configuración

- `pythonpath = ["src"]` en `pyproject.toml` permite importar `backend.*` desde los tests.
- `testpaths = ["tests"]` define la carpeta de tests por defecto.
- `.vscode/settings.json` configura Pylance para resolver importaciones correctamente.
