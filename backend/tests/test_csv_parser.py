from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from backend.conciliacion.csv_parser import (
    ErrorCSV,
    parsear_contabilidad,
    parsear_facturas,
)


# parsear_facturas

def test_parsear_facturas_valido():
    csv = b"id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nF001,123456789,2024-01-15,Compra,1000,0.19,190,0.10,100,1090"
    facturas = parsear_facturas(csv)
    assert len(facturas) == 1
    assert facturas[0].id_factura == "F001"
    assert facturas[0].base_gravable == Decimal("1000")
    assert facturas[0].fecha_factura == date(2024, 1, 15)


def test_parsear_facturas_vacio():
    with pytest.raises(ErrorCSV, match="vacío"):
        parsear_facturas(b"")


def test_parsear_facturas_columna_faltante():
    csv = b"id_factura,nit_proveedor\nF001,123456789"
    with pytest.raises(ErrorCSV, match="columna requerida"):
        parsear_facturas(csv)


def test_parsear_facturas_fecha_invalida():
    csv = b"id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nF001,123456789,15-01-2024,Compra,1000,0.19,190,0.10,100,1090"
    facturas = parsear_facturas(csv)
    assert facturas[0].fecha_factura is None


def test_parsear_facturas_fecha_vacia():
    csv = b"id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nF001,123456789,,Compra,1000,0.19,190,0.10,100,1090"
    facturas = parsear_facturas(csv)
    assert facturas[0].fecha_factura is None


def test_parsear_facturas_valor_numerico_invalido():
    csv = b"id_factura,nit_proveedor,fecha_factura,concepto,base_gravable,tarifa_iva,valor_iva,tarifa_retencion,valor_retencion,total_factura\nF001,123456789,2024-01-15,Compra,abc,0.19,190,0.10,100,1090"
    with pytest.raises(ErrorCSV, match="Valor numérico inválido"):
        parsear_facturas(csv)


# parsear_contabilidad

def test_parsear_contabilidad_valido():
    csv = b"id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado\nF001,2024-01-16,110505,CC01,1090,0,Contabilizada"
    registros = parsear_contabilidad(csv)
    assert len(registros) == 1
    assert registros[0].id_factura == "F001"
    assert registros[0].estado == "Contabilizada"
    assert registros[0].fecha_contabilizacion == date(2024, 1, 16)


def test_parsear_contabilidad_vacio():
    with pytest.raises(ErrorCSV, match="vacío"):
        parsear_contabilidad(b"")


def test_parsear_contabilidad_columna_faltante():
    csv = b"id_factura,fecha_contabilizacion\nF001,2024-01-16"
    with pytest.raises(ErrorCSV, match="columna requerida"):
        parsear_contabilidad(csv)


def test_parsear_contabilidad_fecha_invalida():
    csv = b"id_factura,fecha_contabilizacion,cuenta_contable,centro_costo,valor_debito,valor_credito,estado\nF001,16-01-2024,110505,CC01,1090,0,Contabilizada"
    registros = parsear_contabilidad(csv)
    assert registros[0].fecha_contabilizacion is None
