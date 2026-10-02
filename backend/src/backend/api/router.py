from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.conciliacion.csv_parser import (
    ErrorCSV,
    parsear_contabilidad,
    parsear_facturas,
)
from backend.conciliacion.service import conciliar

router = APIRouter()


@router.post("/conciliacion")
async def conciliacion_endpoint(
    facturas: UploadFile = File(...),
    contabilidad: UploadFile = File(...),
):
    try:
        facturas_data = parsear_facturas(await facturas.read())
        contabilidad_data = parsear_contabilidad(await contabilidad.read())
    except ErrorCSV as e:
        raise HTTPException(status_code=400, detail=str(e))

    resultado = conciliar(facturas_data, contabilidad_data)

    return {
        "resumen": {
            "total_facturas": resultado.resumen.total_facturas,
            "correctas": resultado.resumen.correctas,
            "inconsistencias": resultado.resumen.inconsistencias,
        },
        "detalles": [
            {
                "id_factura_linea": d.id_factura_linea,
                "id_factura": d.id_factura,
                "estado": d.estado,
                "causas": [c.value for c in d.causas],
            }
            for d in resultado.detalles
        ],
    }
