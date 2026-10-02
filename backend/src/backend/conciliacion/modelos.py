from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class CausaInconsistencia(str, Enum):
    IVA_INCORRECTO = "IVA incorrecto"
    RETENCION_INCORRECTA = "Retención incorrecta"
    TOTAL_INCORRECTO = "Total de factura incorrecto"
    FACTURA_DUPLICADA = "Factura duplicada"
    REGISTRO_DUPLICADO = "Registro contable duplicado"
    SIN_CONTABILIZACION = "Factura sin registro en contabilidad"
    ESTADO_CONTABLE_INVALIDO = "Estado contable inválido"
    FORMATO_FECHA_INVALIDO = "Formato de fecha inválido"


@dataclass
class Factura:
    id_factura_linea: str
    id_factura: str
    nit_proveedor: str
    fecha_factura: date | None
    concepto: str
    base_gravable: Decimal
    tarifa_iva: Decimal
    valor_iva: Decimal
    tarifa_retencion: Decimal
    valor_retencion: Decimal
    total_factura: Decimal


@dataclass
class RegistroContable:
    id_factura: str
    fecha_contabilizacion: date | None
    cuenta_contable: str
    centro_costo: str
    valor_debito: Decimal
    valor_credito: Decimal
    estado: str


@dataclass
class Detalle:
    id_factura_linea: str
    id_factura: str
    estado: str
    causas: list[CausaInconsistencia] = field(default_factory=list)


@dataclass
class Resumen:
    total_facturas: int
    correctas: int
    inconsistencias: int


@dataclass
class ResultadoConciliacion:
    resumen: Resumen
    detalles: list[Detalle]
