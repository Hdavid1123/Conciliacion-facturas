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

## Pendientes

- Revisar TEST-CASES.md.
- Resolver cualquier ambigüedad de formato de tarifas y precisión antes de implementar las reglas afectadas.
EOF