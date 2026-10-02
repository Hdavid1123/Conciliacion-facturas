import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ConciliacionService, ResultadoConciliacion } from './conciliacion.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrls: ['./app.css'],
})
export class App {
  private conciliacionService = inject(ConciliacionService);

  loading = signal(false);
  error = signal<string | null>(null);
  resultado = signal<ResultadoConciliacion | null>(null);
  filtro = signal<'todos' | 'correctas' | 'inconsistencias'>('todos');

  facturasFile: File | null = null;
  contabilidadFile: File | null = null;

  onFacturasChange(event: Event) {
    const input = event.target as HTMLInputElement;
    this.facturasFile = input.files?.[0] ?? null;
  }

  onContabilidadChange(event: Event) {
    const input = event.target as HTMLInputElement;
    this.contabilidadFile = input.files?.[0] ?? null;
  }

  async procesar() {
    if (!this.facturasFile || !this.contabilidadFile) {
      this.error.set('Debe seleccionar ambos archivos');
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.resultado.set(null);

    this.conciliacionService.conciliar(this.facturasFile, this.contabilidadFile).subscribe({
      next: (resultado) => {
        this.resultado.set(resultado);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Error desconocido');
        this.loading.set(false);
      },
    });
  }

  detallesFiltrados() {
    const resultado = this.resultado();
    if (!resultado) return [];
    const filtro = this.filtro();
    if (filtro === 'correctas') return resultado.detalles.filter(d => d.estado === 'Correcta');
    if (filtro === 'inconsistencias') return resultado.detalles.filter(d => d.estado === 'Con inconsistencia');
    return resultado.detalles;
  }
}
