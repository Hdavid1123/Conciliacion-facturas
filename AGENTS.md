# AGENTS.md

Prototipo web de conciliación de facturas. Encargado de carga archivos CSV, procesarlos según las reglas de `specs/SPEC.md` y consultar un resumen y detalle mediante una interfaz simple.

## Stack y estructura

### Backend: Python + FastAPI

FastAPI debe:

- Recibir y validar archivos.
- Invocar el servicio de conciliación.
- Convertir errores conocidos en respuestas HTTP.
- Devolver JSON.

No colocar la lógica de negocio en los routers.

### Frontend: Angular

Mantener el frontend pequeño. Debe permitir:

- Cargar los archivos CSV requeridos.
- Ejecutar el procesamiento.
- Mostrar loading, errores, resumen y resultados.
- Filtrar resultados por estado.

No crear componentes, servicios o abstracciones innecesarias.

### Arquitectura

Separar como mínimo HTTP/API, servicio de conciliación y reglas de negocio. La conciliación no debe depender de FastAPI y debe poder probarse sin iniciar el servidor.

No implementar base de datos, ORM, persistencia, autenticación, usuarios, Redis, Docker, microservicios ni infraestructura no solicitada.

## Forma de trabajar

Actúa como agente de desarrollo del proyecto. Implementa lo definido en las especificaciones; no redefinas los requisitos.

Evita abstracciones prematuras, patrones innecesarios, clases creadas por formalidad, duplicación y comentarios que solo repitan el código.

## Límites

Antes de modificar código, leer:

1. `specs/SPEC.md`
2. `specs/API.md`
3. `specs/TEST-CASES.md`

No agregar funcionalidades no justificadas por las especificaciones. Si código existente contradice una especificación, identificar la contradicción en lugar de asumir que el código es correcto.

Ante ambigüedades, documentar el supuesto y no inventar requisitos. Cambiar únicamente lo necesario para cumplir la tarea solicitada.

Leer `MEMORY.md` al iniciar una tarea y actualizarlo al terminar.

## Reglas de negocio

Implementar únicamente las reglas definidas en `specs/SPEC.md`. No inferir reglas adicionales por el nombre de los campos.

La existencia de `valor_debito`, `valor_credito` o `estado` en `contabilidad.csv` no implica validaciones adicionales si estas no están especificadas.

Ante una posible regla nueva, documentar la duda y solicitar una decisión antes de implementarla.

## Precisión numérica

Usar un mecanismo apropiado para valores decimales y evitar errores monetarios derivados del punto flotante.

Respetar la precisión definida en `SPEC.md` y no introducir tolerancias arbitrarias sin documentarlas.

## Tests

Toda regla de negocio debe tener pruebas.

Antes de terminar una modificación:

1. Ejecutar los tests relevantes.
2. Ejecutar la suite completa.
3. Corregir los fallos.
4. No eliminar ni debilitar tests para conseguir una suite verde.

Los tests deben validar comportamiento y no detalles internos innecesarios.

## Memoria

`MEMORY.md` debe mantenerse breve, máximo ~50 líneas, y contener solo estado, decisiones importantes con su motivo y errores a evitar.

Eliminar o resumir información obsoleta. No guardar claves, tokens ni datos personales.

Si una decisión se convierte en regla permanente, proponer moverla a `AGENTS.md`.

## Dependencias

El backend utiliza `uv` para gestionar dependencias y el entorno Python.

Mantener las dependencias al mínimo necesario para cumplir `SPEC.md`. Antes de agregar una dependencia, verificar si puede utilizarse la biblioteca estándar o una dependencia existente.

No agregar dependencias por conveniencia arquitectónica o preferencias personales.

Toda dependencia debe declararse en `pyproject.toml` y `uv.lock` debe mantenerse actualizado. No utilizar `pip` manualmente como parte del flujo normal.

## Verificación final

Antes de considerar terminado el proyecto, verificar:

- Las funcionalidades cumplen `SPEC.md`.
- La API cumple `API.md`.
- Los casos definidos en `TEST-CASES.md` están cubiertos.
- Los tests pasan.
- No existen funcionalidades fuera del alcance.
- Las dependencias son las mínimas necesarias.
- La documentación refleja las decisiones implementadas.
