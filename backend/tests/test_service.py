from __future__ import annotations

from datetime import date
from decimal import Decimal

from backend.conciliacion.modelos import (
    CausaInconsistencia,
    Factura,
    RegistroContable,
)
from backend.conciliacion.service import conciliar


def _factura(**kwargs) -> Factura:
    return Factura(
        id_factura=kwargs.get("id_factura", "F001"),
        nit_proveedor=kwargs.get("nit_proveedor", "123456789"),
        fecha_factura=kwargs.get("fecha_factura", date(2024, 1, 15)),
        concepto=kwargs.get("concepto", "Compra"),
        base_gravable=kwargs.get("base_gravable", Decimal("1000")),
        tarifa_iva=kwargs.get("tarifa_iva", Decimal("0.19")),
        valor_iva=kwargs.get("valor_iva", Decimal("190")),
        tarifa_retencion=kwargs.get("tarifa_retencion", Decimal("0.10")),
        valor_retencion=kwargs.get("valor_retencion", Decimal("100")),
        total_factura=kwargs.get("total_factura", Decimal("1090")),
    )


def _registro(**kwargs) -> RegistroContable:
    return RegistroContable(
        id_factura=kwargs.get("id_factura", "F001"),
        fecha_contabilizacion=kwargs.get("fecha_contabilizacion", date(2024, 1, 16)),
        cuenta_contable=kwargs.get("cuenta_contable", "110505"),
        centro_costo=kwargs.get("centro_costo", "CC01"),
        valor_debito=kwargs.get("valor_debito", Decimal("1090")),
        valor_credito=kwargs.get("valor_credito", Decimal("0")),
        estado=kwargs.get("estado", "Contabilizada"),
    )


# TC-15 - total_facturas = N

def test_conciliar_total_facturas():
    facturas = [
        _factura(id_factura="F001"),
        _factura(id_factura="F002"),
        _factura(id_factura="F003"),
    ]
    registros = [
        _registro(id_factura="F001"),
        _registro(id_factura="F002"),
        _registro(id_factura="F003"),
    ]
    resultado = conciliar(facturas, registros)
    assert resultado.resumen.total_facturas == 3


# TC-16 - correctas + inconsistencias = total_facturas

def test_conciliar_suma_correctas_inconsistencias():
    facturas = [
        _factura(id_factura="F001"),
        _factura(id_factura="F002", valor_iva=Decimal("200")),
    ]
    registros = [
        _registro(id_factura="F001"),
        _registro(id_factura="F002"),
    ]
    resultado = conciliar(facturas, registros)
    assert resultado.resumen.correctas + resultado.resumen.inconsistencias == resultado.resumen.total_facturas


# TC-17 - Resumen coincide con detalle

def test_conciliar_resumen_coincide_con_detalle():
    facturas = [
        _factura(id_factura="F001"),
        _factura(id_factura="F002", valor_iva=Decimal("200")),
        _factura(id_factura="F003"),
    ]
    registros = [
        _registro(id_factura="F001"),
        _registro(id_factura="F002"),
        _registro(id_factura="F003"),
    ]
    resultado = conciliar(facturas, registros)

    correctas = sum(1 for d in resultado.detalles if d.estado == "Correcta")
    inconsistencias = sum(1 for d in resultado.detalles if d.estado == "Con inconsistencia")

    assert resultado.resumen.correctas == correctas
    assert resultado.resumen.inconsistencias == inconsistencias


# TC-01 - Factura correcta (integración)

def test_conciliar_factura_correcta():
    facturas = [_factura(id_factura="F001")]
    registros = [_registro(id_factura="F001")]
    resultado = conciliar(facturas, registros)

    assert len(resultado.detalles) == 1
    assert resultado.detalles[0].id_factura == "F001"
    assert resultado.detalles[0].estado == "Correcta"
    assert resultado.detalles[0].causas == []


# TC-08 - Múltiples inconsistencias

def test_conciliar_multiples_inconsistencias():
    facturas = [_factura(id_factura="F001", valor_iva=Decimal("200"), total_factura=Decimal("1200"))]
    registros = [_registro(id_factura="F001", estado="Anulado")]
    resultado = conciliar(facturas, registros)

    assert len(resultado.detalles) == 1
    assert resultado.detalles[0].estado == "Con inconsistencia"
    assert CausaInconsistencia.IVA_INCORRECTO in resultado.detalles[0].causas
    assert CausaInconsistencia.TOTAL_INCORRECTO in resultado.detalles[0].causas
    assert CausaInconsistencia.ESTADO_CONTABLE_INVALIDO in resultado.detalles[0].causas
