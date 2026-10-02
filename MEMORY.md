cat > MEMORY.md <<'EOF'
# MEMORY

## Estado

Backend completo. Pendiente implementar frontend Angular.

## Decisiones

- Backend gestionado con uv.
- Conciliación independiente de FastAPI.
- Sin base de datos ni persistencia.
- La lógica debe seguir SPEC.md sin inferir reglas adicionales.
- Angular se mantiene como frontend pequeño.
- R2: retención = base_gravable × tarifa_retencion; si no coincide, es inconsistencia.
- R5: registros contables duplicados → inconsistencia. No tomar registro silenciosamente.
- R8: `estado` en contabilidad.csv debe ser `Pendiente` o `Contabilizada`; si no, es inconsistencia.
- R9: fechas con formato `yyyy-mm-dd`; si no, es inconsistencia. Parser no rechaza, identifica factura afectada.
- id_factura_linea: identificador único por posición en el archivo. Permite distinguir duplicados. Formato: `{id_factura}_L{#}`.

## Pendientes

- Implementar frontend Angular.
- Escribir tests de integración e2e para el frontend.
EOF