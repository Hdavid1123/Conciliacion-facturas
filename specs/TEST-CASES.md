# Casos de prueba — Conciliador de facturas

## Objetivo

Cubrir mediante pruebas automatizadas y manuales las reglas de negocio, validaciones, cálculos e integración del conciliador.

## Reglas de negocio

* TC-01 Factura correcta: IVA, retención y total coinciden, no hay duplicidad y existe registro contable. Estado: `Correcta`; inconsistencias: `[]`.
* TC-02 IVA incorrecto: detectar `IVA calculado diferente al esperado`.
* TC-03 Retención incorrecta: detectar `Retención calculada diferente al esperado`.
* TC-04 Total incorrecto: detectar `Total calculado diferente al esperado`.
* TC-05 Factura duplicada: mismo `id_factura`; detectar `Factura duplicada`.
* TC-06 Sin registro contable: factura sin coincidencia en contabilidad; detectar `Factura sin registro en contabilidad`.
* TC-07 Múltiples inconsistencias: detectar todas las condiciones inválidas sin detenerse en la primera.
* TC-08 Estado contable inválido: registro con `estado` diferente de `Pendiente` o `Contabilizada`; detectar `Estado contable inválido`.
* TC-09 Formato de fecha inválido: `fecha_factura` o `fecha_contabilizacion` sin formato `yyyy-mm-dd` o sin valor; detectar `Formato de fecha inválido`.

## Validaciones

* TC-10 Falta archivo de facturas: devolver error HTTP indicando el archivo requerido.
* TC-11 Falta archivo de contabilidad: devolver error HTTP indicando el archivo requerido.
* TC-12 Columnas obligatorias ausentes: devolver error claro y no procesar silenciosamente.
* TC-13 CSV inválido o ilegible: devolver error claro, sin resultados parciales silenciosos.

## Resumen

* TC-14 Para N facturas: `total_facturas = N`.
* TC-15 Debe cumplirse `correctas + inconsistencias = total_facturas`.
* TC-16 El resumen debe coincidir con los estados de `details`.

## Cálculos

* TC-17 Con base 1000 y tarifa IVA 19%, IVA esperado = 190. Si `valor_iva = 190`, no hay inconsistencia.
* TC-18 Con base 1000, IVA 190 y retención 10, total esperado = 1180. Si `total_factura = 1180`, no hay inconsistencia.

## Integración

Debe existir una prueba del flujo:
`CSV → endpoint FastAPI → parsing → servicio de conciliación → JSON`.
Debe validar `summary`, `details`, estados e inconsistencias.

* TC-19 Integración: prueba del flujo completo `CSV → endpoint FastAPI → parsing → servicio de conciliación → JSON`.

## Pruebas manuales

Ejecutar: archivo válido, IVA incorrecto, retención incorrecto, total incorrecto, duplicados, factura sin contabilidad, múltiples inconsistencias, columnas faltantes, procesamiento sin ambos archivos y filtros `Todos`, `Correctas` y `Con inconsistencia`.

## Criterio de finalización

Todos los tests automatizados deben pasar y los escenarios manuales críticos deben ejecutarse. Compilar o arrancar la aplicación no es suficiente; el comportamiento debe corresponder con `SPEC.md`.
