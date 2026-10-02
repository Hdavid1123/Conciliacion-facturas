from __future__ import annotations

from datetime import date
from decimal import Decimal

from backend.conciliacion.modelos import (
    CausaInconsistencia,
    Factura,
    RegistroContable,
)
from backend.conciliacion.reglas import (
    r1_iva,
    r2_retencion,
    r3_total,
    r4_duplicados,
    r5_registro_duplicado,
    r6_sin_contabilizacion,
    r7_clasificacion,
    r8_estado_contable,
    r9_fechas,
)


def _factura(**kwargs) -> Factura:
    return Factura(
        id_factura_linea=kwargs.get("id_factura_linea", "F001_L1"),
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


# R1 - IVA

def test_r1_iva_correcto():
    factura = _factura(base_gravable=Decimal("1000"), tarifa_iva=Decimal("0.19"), valor_iva=Decimal("190"))
    assert r1_iva(factura) == []


def test_r1_iva_incorrecto():
    factura = _factura(base_gravable=Decimal("1000"), tarifa_iva=Decimal("0.19"), valor_iva=Decimal("200"))
    assert r1_iva(factura) == [CausaInconsistencia.IVA_INCORRECTO]


# R2 - Retención

def test_r2_retencion_correcta():
    factura = _factura(base_gravable=Decimal("1000"), tarifa_retencion=Decimal("0.10"), valor_retencion=Decimal("100"))
    assert r2_retencion(factura) == []


def test_r2_retencion_incorrecta():
    factura = _factura(base_gravable=Decimal("1000"), tarifa_retencion=Decimal("0.10"), valor_retencion=Decimal("150"))
    assert r2_retencion(factura) == [CausaInconsistencia.RETENCION_INCORRECTA]


# R3 - Total

def test_r3_total_correcto():
    factura = _factura(
        base_gravable=Decimal("1000"),
        valor_iva=Decimal("190"),
        valor_retencion=Decimal("100"),
        total_factura=Decimal("1090"),
    )
    assert r3_total(factura) == []


def test_r3_total_incorrecto():
    factura = _factura(
        base_gravable=Decimal("1000"),
        valor_iva=Decimal("190"),
        valor_retencion=Decimal("100"),
        total_factura=Decimal("1200"),
    )
    assert r3_total(factura) == [CausaInconsistencia.TOTAL_INCORRECTO]


# R4 - Facturas duplicadas

def test_r4_duplicados_sin_duplicados():
    facturas = [_factura(id_factura="F001", id_factura_linea="F001_L1"), _factura(id_factura="F002", id_factura_linea="F002_L2")]
    assert r4_duplicados(facturas) == {}


def test_r4_duplicados_con_duplicado():
    facturas = [_factura(id_factura="F001", id_factura_linea="F001_L1"), _factura(id_factura="F001", id_factura_linea="F001_L3")]
    assert r4_duplicados(facturas) == {"F001": [CausaInconsistencia.FACTURA_DUPLICADA]}


# R5 - Registro contable duplicado

def test_r5_registro_duplicado_sin_duplicados():
    registros = [_registro(id_factura="F001"), _registro(id_factura="F002")]
    assert r5_registro_duplicado(registros) == {}


def test_r5_registro_duplicado_con_duplicado():
    registros = [_registro(id_factura="F001"), _registro(id_factura="F001")]
    assert r5_registro_duplicado(registros) == {"F001": [CausaInconsistencia.REGISTRO_DUPLICADO]}


# R6 - Sin contabilización

def test_r6_sin_contabilizacion_todas_con_registro():
    facturas = [_factura(id_factura="F001")]
    registros = [_registro(id_factura="F001")]
    assert r6_sin_contabilizacion(facturas, registros) == {}


def test_r6_sin_contabilizacion_una_sin_registro():
    facturas = [_factura(id_factura="F001"), _factura(id_factura="F002")]
    registros = [_registro(id_factura="F001")]
    assert r6_sin_contabilizacion(facturas, registros) == {
        "F002": [CausaInconsistencia.SIN_CONTABILIZACION]
    }


# R7 - Clasificación

def test_r7_clasificacion_correcta():
    assert r7_clasificacion([]) == "Correcta"


def test_r7_clasificacion_inconsistente():
    assert r7_clasificacion([CausaInconsistencia.IVA_INCORRECTO]) == "Con inconsistencia"


# R8 - Estado contable

def test_r8_estado_contable_valido():
    registro = _registro(estado="Contabilizada")
    assert r8_estado_contable(registro) == []


def test_r8_estado_contable_invalido():
    registro = _registro(estado="Anulado")
    assert r8_estado_contable(registro) == [CausaInconsistencia.ESTADO_CONTABLE_INVALIDO]


# R9 - Formato de fechas

def test_r9_fechas_correctas():
    factura = _factura(fecha_factura=date(2024, 1, 15))
    registro = _registro(fecha_contabilizacion=date(2024, 1, 16))
    assert r9_fechas(factura, registro) == []


def test_r9_fechas_factura_invalida():
    factura = _factura(fecha_factura=None)
    registro = _registro(fecha_contabilizacion=date(2024, 1, 16))
    assert r9_fechas(factura, registro) == [CausaInconsistencia.FORMATO_FECHA_INVALIDO]


def test_r9_fechas_registro_invalida():
    factura = _factura(fecha_factura=date(2024, 1, 15))
    registro = _registro(fecha_contabilizacion=None)
    assert r9_fechas(factura, registro) == [CausaInconsistencia.FORMATO_FECHA_INVALIDO]


def test_r9_fechas_sin_registro():
    factura = _factura(fecha_factura=date(2024, 1, 15))
    assert r9_fechas(factura, None) == []
