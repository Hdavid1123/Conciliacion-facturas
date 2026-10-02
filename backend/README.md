# Backend — Conciliador de Facturas

## Ejecución

```bash
uv run uvicorn backend.main:app --reload
```

## Tests

### Ejecutar todos los tests

```bash
uv run python -m pytest
```

### Ejecutar un archivo específico

```bash
uv run python -m pytest tests/test_reglas.py
uv run python -m pytest tests/test_csv_parser.py
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
| `tests/test_reglas.py` | 18 | R1–R8 (reglas de negocio) |
| `tests/test_csv_parser.py` | 10 | Parseo y validación de CSV |
| `tests/test_service.py` | — | Pendiente |
| `tests/test_api.py` | — | Pendiente |

## Configuración

- `pythonpath = ["src"]` en `pyproject.toml` permite importar `backend.*` desde los tests.
- `testpaths = ["tests"]` define la carpeta de tests por defecto.
