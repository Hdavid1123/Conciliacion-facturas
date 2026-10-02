from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

CSV_FACTURAS = b"id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nF001,123456789,2024-01-15,Compra,1000,0.19,190,0.10,100,1090"

CSV_CONTABILIDAD = b"id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado\nF001,2024-01-16,110505,CC01,1090,0,Contabilizada"


# TC-11 - Falta archivo de facturas

def test_api_falta_archivo_facturas():
    response = client.post(
        "/api/conciliacion",
        files={"contabilidad": ("contabilidad.csv", CSV_CONTABILIDAD)},
    )
    assert response.status_code == 422


# TC-12 - Falta archivo de contabilidad

def test_api_falta_archivo_contabilidad():
    response = client.post(
        "/api/conciliacion",
        files={"facturas": ("facturas.csv", CSV_FACTURAS)},
    )
    assert response.status_code == 422


# TC-20 - Integración e2e

def test_api_integracion_e2e():
    response = client.post(
        "/api/conciliacion",
        files={
            "facturas": ("facturas.csv", CSV_FACTURAS),
            "contabilidad": ("contabilidad.csv", CSV_CONTABILIDAD),
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "resumen" in data
    assert "detalles" in data

    resumen = data["resumen"]
    assert resumen["total_facturas"] == 1
    assert resumen["correctas"] == 1
    assert resumen["inconsistencias"] == 0

    detalles = data["detalles"]
    assert len(detalles) == 1
    assert detalles[0]["id_factura_linea"] == "F001_L1"
    assert detalles[0]["id_factura"] == "F001"
    assert detalles[0]["estado"] == "Correcta"
    assert detalles[0]["causas"] == []


# TC-13 - Columnas obligatorias ausentes

def test_api_columna_faltante():
    csv_sin_columna = b"id_factura,nit_proveedor\nF001,123456789"
    response = client.post(
        "/api/conciliacion",
        files={
            "facturas": ("facturas.csv", csv_sin_columna),
            "contabilidad": ("contabilidad.csv", CSV_CONTABILIDAD),
        },
    )
    assert response.status_code == 400
    assert "columna requerida" in response.json()["detail"]


# TC-14 - CSV inválido o ilegible

def test_api_csv_vacio():
    response = client.post(
        "/api/conciliacion",
        files={
            "facturas": ("facturas.csv", b""),
            "contabilidad": ("contabilidad.csv", CSV_CONTABILIDAD),
        },
    )
    assert response.status_code == 400
    assert "vacío" in response.json()["detail"]
