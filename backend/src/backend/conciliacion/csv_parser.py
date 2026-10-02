from __future__ import annotations

import csv
import io
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from backend.conciliacion.modelos import Factura, RegistroContable


COLUMNAS_FACTURAS = [
    "id_factura",
    "nit_proveedor",
    "fecha_factura",
    "concepto",
    "base_gravable",
    "tarifa_iva",
    "valor_iva",
    "tarifa_retencion",
    "valor_retencion",
    "total_factura",
]

COLUMNAS_CONTABILIDAD = [
    "id_factura",
    "fecha_contabilizacion",
    "cuenta_contable",
    "centro_costo",
    "valor_debito",
    "valor_credito",
    "estado",
]


class ErrorCSV(Exception):
    """Error de validación del CSV (columnas faltantes, archivo vacío, etc.)."""


def _leer_csv(data: bytes, nombre: str, columnas_requeridas: list[str]) -> list[dict[str, str]]:
    if not data or not data.strip():
        raise ErrorCSV(f"El archivo {nombre} está vacío")

    try:
        texto = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ErrorCSV(f"El archivo {nombre} no es un CSV válido (codificación)")

    reader = csv.DictReader(io.StringIO(texto))
    if reader.fieldnames is None:
        raise ErrorCSV(f"El archivo {nombre} no tiene encabezados")

    columnas_faltantes = [c for c in columnas_requeridas if c not in reader.fieldnames]
    if columnas_faltantes:
        raise ErrorCSV(
            f"El archivo {nombre} no contiene la columna requerida: {columnas_faltantes[0]}"
        )

    filas = list(reader)
    if not filas:
        raise ErrorCSV(f"El archivo {nombre} está vacío")

    return filas


def _fila_a_factura(fila: dict[str, str], linea: int) -> Factura:
    id_factura = fila["id_factura"]
    return Factura(
        id_factura_linea=f"{id_factura}_L{linea}",
        id_factura=id_factura,
        nit_proveedor=fila["nit_proveedor"],
        fecha_factura=_parsear_fecha(fila["fecha_factura"]),
        concepto=fila["concepto"],
        base_gravable=_parsear_decimal(fila["base_gravable"]),
        tarifa_iva=_parsear_decimal(fila["tarifa_iva"]),
        valor_iva=_parsear_decimal(fila["valor_iva"]),
        tarifa_retencion=_parsear_decimal(fila["tarifa_retencion"]),
        valor_retencion=_parsear_decimal(fila["valor_retencion"]),
        total_factura=_parsear_decimal(fila["total_factura"]),
    )


def _fila_a_registro(fila: dict[str, str]) -> RegistroContable:
    return RegistroContable(
        id_factura=fila["id_factura"],
        fecha_contabilizacion=_parsear_fecha(fila["fecha_contabilizacion"]),
        cuenta_contable=fila["cuenta_contable"],
        centro_costo=fila["centro_costo"],
        valor_debito=_parsear_decimal(fila["valor_debito"]),
        valor_credito=_parsear_decimal(fila["valor_credito"]),
        estado=fila["estado"],
    )


def _parsear_decimal(valor: str) -> Decimal:
    try:
        return Decimal(valor)
    except InvalidOperation:
        raise ErrorCSV(f"Valor numérico inválido: {valor}")


def _parsear_fecha(valor: str) -> date | None:
    if not valor or not valor.strip():
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


def parsear_facturas(data: bytes) -> list[Factura]:
    filas = _leer_csv(data, "facturas.csv", COLUMNAS_FACTURAS)
    return [_fila_a_factura(f, i) for i, f in enumerate(filas, start=1)]


def parsear_contabilidad(data: bytes) -> list[RegistroContable]:
    filas = _leer_csv(data, "contabilidad.csv", COLUMNAS_CONTABILIDAD)
    return [_fila_a_registro(f) for f in filas]
