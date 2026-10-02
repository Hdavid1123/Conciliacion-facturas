# SPEC.md

Especificación funcional del prototipo de conciliación de facturas.

## Objetivo

Cargar un archivo de facturas y uno contable, aplicar reglas de conciliación y mostrar resumen y detalle de inconsistencias.

## Alcance

El sistema debe:

- Recibir `facturas.csv` y `contabilidad.csv`.
- Validar estructura y campos requeridos.
- Procesar las reglas de conciliación.
- Clasificar facturas como `Correcta` o `Con inconsistencia`.
- Indicar las causas detectadas.
- Mostrar resumen y detalle.
- Permitir filtrar el detalle por estado.

No se requiere persistencia, base de datos, historial ni procesamiento posterior.

## Archivos de entrada

`facturas.csv` requiere:
`id_factura`, `nit_proveedor`, `fecha_factura`, `concepto`, `base_gravable`, `tarifa_iva`, `valor_iva`, `tarifa_retencion`, `valor_retencion`, `total_factura`.

`contabilidad.csv` requiere:
`id_factura`, `fecha_contabilizacion`, `cuenta_contable`, `centro_costo`, `valor_debito`, `valor_credito`, `estado`.

`id_factura` relaciona ambos archivos. La existencia de un campo no implica validaciones adicionales.

## Reglas de negocio

### R1. IVA

IVA esperado = `base_gravable × tarifa_iva`.
Comparar el resultado con `valor_iva`.

### R2. Retención

Retención esperada = `base_gravable × tarifa_retencion`.
Comparar el resultado con `valor_retencion`.

### R3. Total

Total esperado = `base_gravable + valor_iva - valor_retencion`.
Comparar con `total_factura`.

### R4. Facturas duplicadas

Identificar facturas duplicadas según `id_factura` y clasificarlas como inconsistentes.

### R5. Registro contable duplicado

Si un `id_factura` aparece más de una vez en `contabilidad.csv`, clasificar la factura como inconsistente con la causa `Registro contable duplicado`.

### R6. Sin contabilización

Identificar facturas cuyo `id_factura` no exista en `contabilidad.csv` y clasificarlas como inconsistentes.

### R7. Clasificación

Sin inconsistencias → `Correcta`.
Una o más inconsistencias → `Con inconsistencia`.
Si existen varias, indicar todas las causas detectadas.

### R8. Estado contable

Si el registro contable asociado tiene `estado` diferente de `Pendiente` o `Contabilizada`, clasificar la factura como inconsistente con la causa `Estado contable inválido`.

### R9. Formato de fechas

Las columnas `fecha_factura` y `fecha_contabilizacion` deben tener formato `yyyy-mm-dd`. Si una entrada no tiene el formato adecuado o no hay valor, clasificar la factura como inconsistente con la causa `Formato de fecha inválido`. El parser no rechaza el archivo; identifica la factura afectada.

## Precisión

Usar representación decimal adecuada para valores monetarios y evitar errores de punto flotante. No introducir tolerancias arbitrarias. Si se requiere redondeo, debe documentarse y aplicarse consistentemente.

## Validaciones

Rechazar archivos faltantes, vacíos, no procesables o sin columnas requeridas. Los errores de entrada deben diferenciarse de las inconsistencias de negocio.

## Resultado

El resultado debe incluir:

- Total de facturas.
- Cantidad de correctas.
- Cantidad de inconsistencias.
- Detalle por factura.
- Estado.
- Causas, cuando existan.

El resumen debe coincidir con el detalle.

## Interfaz

El frontend debe permitir cargar archivos, ejecutar el procesamiento, mostrar loading, errores, resumen y detalle, y filtrar por estado.

## Flujo

`CSV → validación → parseo → conciliación → clasificación → resumen/detalle → API`

La lógica de conciliación debe ser independiente de HTTP.

## Aceptación

El prototipo es funcional cuando los archivos pueden procesarse, las columnas son validadas, R1–R9 producen los resultados definidos, el resumen coincide con el detalle y el frontend muestra y filtra los resultados.
