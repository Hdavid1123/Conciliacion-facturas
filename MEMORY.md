cat > MEMORY.md <<'EOF'
# MEMORY

## Estado

Proyecto inicializado. Pendiente implementar backend FastAPI, conciliación, frontend Angular y pruebas.

## Decisiones

- Backend gestionado con uv.
- Conciliación independiente de FastAPI.
- Sin base de datos ni persistencia.
- La lógica debe seguir SPEC.md sin inferir reglas adicionales.
- Angular se mantiene como frontend pequeño.
- R2: retención = base_gravable × tarifa_retencion; si no coincide, es inconsistencia.
- R7: `estado` en contabilidad.csv debe ser `Pendiente` o `Contabilizada`; si no, es inconsistencia.
- R8: fechas con formato `yyyy-mm-dd`; si no, es inconsistencia. Parser no rechaza, identifica factura afectada.

## Pendientes

- Implementar backend (modelos, parser, reglas, servicio, API).
- Implementar frontend Angular.
- Escribir tests de reglas, parser, servicio e integración.
EOF