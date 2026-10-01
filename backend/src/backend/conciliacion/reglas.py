from __future__ import annotations

from collections import Counter

from backend.conciliacion.modelos import (
    CausaInconsistencia,
    Factura,
    RegistroContable,
)


def r1_iva(factura: Factura) -> list[CausaInconsistencia]:
    esperado = factura.base_gravable * factura.tarifa_iva
    if factura.valor_iva != esperado:
        return [CausaInconsistencia.IVA_INCORRECTO]
    return []


def r2_retencion(factura: Factura) -> list[CausaInconsistencia]:
    esperado = factura.base_gravable * factura.tarifa_retencion
    if factura.valor_retencion != esperado:
        return [CausaInconsistencia.RETENCION_INCORRECTA]
    return []


def r3_total(factura: Factura) -> list[CausaInconsistencia]:
    esperado = factura.base_gravable + factura.valor_iva - factura.valor_retencion
    if factura.total_factura != esperado:
        return [CausaInconsistencia.TOTAL_INCORRECTO]
    return []


def r4_duplicados(facturas: list[Factura]) -> dict[str, list[CausaInconsistencia]]:
    conteo = Counter(f.id_factura for f in facturas)
    return {
        id_factura: [CausaInconsistencia.FACTURA_DUPLICADA]
        for id_factura, cantidad in conteo.items()
        if cantidad > 1
    }


def r5_sin_contabilizacion(
    facturas: list[Factura], registros: list[RegistroContable]
) -> dict[str, list[CausaInconsistencia]]:
    ids_contabilidad = {r.id_factura for r in registros}
    return {
        f.id_factura: [CausaInconsistencia.SIN_CONTABILIZACION]
        for f in facturas
        if f.id_factura not in ids_contabilidad
    }


def r6_clasificacion(causas: list[CausaInconsistencia]) -> str:
    return "Con inconsistencia" if causas else "Correcta"


def r7_estado_contable(registro: RegistroContable) -> list[CausaInconsistencia]:
    if registro.estado not in ("Pendiente", "Contabilizada"):
        return [CausaInconsistencia.ESTADO_CONTABLE_INVALIDO]
    return []


def r8_fechas(
    factura: Factura, registro: RegistroContable | None
) -> list[CausaInconsistencia]:
    causas = []
    if factura.fecha_factura is None:
        causas.append(CausaInconsistencia.FORMATO_FECHA_INVALIDO)
    if registro is not None and registro.fecha_contabilizacion is None:
        causas.append(CausaInconsistencia.FORMATO_FECHA_INVALIDO)
    return causas
