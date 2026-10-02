# Frontend — Conciliador de Facturas

## Ejecución

```bash
ng serve
```

La aplicación estará disponible en `http://localhost:4200`.

## Build

```bash
ng build
```

## Tests

### Ejecutar tests

```bash
ng test
```

### Tests del componente (`app.spec.ts`)

| Test | Descripción |
|---|---|
| `should create the app` | Verifica que el componente se crea correctamente |
| `should show error when no files selected` | Verifica error cuando no se seleccionan archivos |
| `should set files on change` | Verifica que los archivos se asignan correctamente |
| `should call service and show result` | Verifica la llamada al servicio y muestra el resultado |
| `should show error when service fails` | Verifica el manejo de errores del servicio |
| `should filter detalles by estado` | Verifica el filtro por estado |

### Tests del servicio (`conciliacion.service.spec.ts`)

| Test | Descripción |
|---|---|
| `should be created` | Verifica que el servicio se crea correctamente |
| `should send POST request with files` | Verifica que se envía la request con los archivos correctos |

## Estructura

```text
src/app/
├── app.ts                      # Componente principal
├── app.html                    # Template
├── app.css                     # Estilos
├── app.config.ts               # Configuración
├── app.routes.ts               # Rutas
├── app.spec.ts                 # Tests del componente
├── conciliacion.service.ts      # Servicio HTTP
└── conciliacion.service.spec.ts # Tests del servicio
```
