import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Detalle {
  id_factura_linea: string;
  id_factura: string;
  estado: string;
  causas: string[];
}

export interface Resumen {
  total_facturas: number;
  correctas: number;
  inconsistencias: number;
}

export interface ResultadoConciliacion {
  resumen: Resumen;
  detalles: Detalle[];
}

@Injectable({ providedIn: 'root' })
export class ConciliacionService {
  private http = inject(HttpClient);
  private url = '/api/conciliacion';

  conciliar(facturas: File, contabilidad: File): Observable<ResultadoConciliacion> {
    const formData = new FormData();
    formData.append('facturas', facturas);
    formData.append('contabilidad', contabilidad);
    return this.http.post<ResultadoConciliacion>(this.url, formData);
  }
}
