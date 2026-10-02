from __future__ import annotations

from backend.conciliacion.modelos import (
    CausaInconsistencia,
    Detalle,
    Factura,
    RegistroContable,
    Resumen,
    ResultadoConciliacion,
)
from backend.conciliacion.reglas import (
    r1_iva,
    r2_retencion,
    r3_total,
    r4_factura_duplicada,
    r5_registro_duplicado,
    r6_sin_contabilizacion,
    r7_clasificacion,
    r8_estado_contable,
    r9_fechas,
)


def conciliar(
    facturas: list[Factura], registros: list[RegistroContable]
) -> ResultadoConciliacion:
    duplicados = r4_factura_duplicada(facturas)
    registros_duplicados = r5_registro_duplicado(registros)
    sin_contabilizacion = r6_sin_contabilizacion(facturas, registros)
    registros_por_id = {r.id_factura: r for r in registros}

    detalles: list[Detalle] = []
    for factura in facturas:
        causas: list[CausaInconsistencia] = []
        causas.extend(r1_iva(factura))
        causas.extend(r2_retencion(factura))
        causas.extend(r3_total(factura))
        causas.extend(duplicados.get(factura.id_factura, []))
        causas.extend(registros_duplicados.get(factura.id_factura, []))
        causas.extend(sin_contabilizacion.get(factura.id_factura, []))

        registro = registros_por_id.get(factura.id_factura)
        if registro is not None:
            causas.extend(r8_estado_contable(registro))
        causas.extend(r9_fechas(factura, registro))

        detalles.append(
            Detalle(
                id_factura=factura.id_factura,
                estado=r7_clasificacion(causas),
                causas=causas,
            )
        )

    correctas = sum(1 for d in detalles if d.estado == "Correcta")
    inconsistencias = len(detalles) - correctas

    return ResultadoConciliacion(
        resumen=Resumen(
            total_facturas=len(facturas),
            correctas=correctas,
            inconsistencias=inconsistencias,
        ),
        detalles=detalles,
    )
