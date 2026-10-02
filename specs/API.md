# API.md

Contrato HTTP entre Angular y FastAPI.

## Base

Base path: `/api`

Las respuestas exitosas y los errores controlados deben utilizar JSON.

## POST `/api/conciliacion`

Recibe `multipart/form-data` con dos campos obligatorios:

* `facturas`: archivo `facturas.csv`.
* `contabilidad`: archivo `contabilidad.csv`.

## Respuesta 200

```json
{
  "resumen": {
    "total_facturas": 50,
    "correctas": 42,
    "inconsistencias": 8
  },
  "detalles": [
    {
      "id_factura_linea": "F001_L1",
      "id_factura": "F001",
      "estado": "Correcta",
      "causas": []
    },
    {
      "id_factura_linea": "F002_L2",
      "id_factura": "F002",
      "estado": "Con inconsistencia",
      "causas": ["IVA incorrecto", "Total de factura incorrecto"]
    }
  ]
}
```

La estructura debe mantenerse alineada con `SPEC.md` y las pruebas.

## Errores

### 400 Bad Request

Para archivos faltantes, vacíos, no procesables o con columnas requeridas ausentes.

Ejemplo:

```json
{"detail": "El archivo facturas.csv no contiene la columna requerida: valor_iva"}
```

### 422 Unprocessable Entity

Para errores de validación de la solicitud detectados por FastAPI.

### 500 Internal Server Error

Solo para errores inesperados. No exponer trazas, detalles internos ni información sensible.

## Responsabilidades

El router debe validar la request, invocar el servicio de conciliación y transformar el resultado a JSON.

La API no debe contener reglas de negocio ni persistir archivos o resultados.

## Frontend

Angular debe:

1. Enviar ambos archivos al endpoint.
2. Mostrar loading durante el procesamiento.
3. Mostrar resumen y detalle.
4. Permitir filtrar por `estado`.
5. Mostrar mensajes comprensibles ante errores.

## Compatibilidad

Los cambios en el contrato deben actualizar `SPEC.md`, `API.md` y las pruebas correspondientes.

No agregar endpoints fuera del alcance definido.
