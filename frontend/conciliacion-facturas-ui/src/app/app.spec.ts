import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { App } from './app';

describe('App', () => {
  let component: App;
  let fixture: ComponentFixture<App>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(App);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it('should show error when no files selected', () => {
    component.procesar();
    expect(component.error()).toBe('Debe seleccionar ambos archivos');
  });

  it('should set files on change', () => {
    const file1 = new File(['content'], 'facturas.csv');
    const file2 = new File(['content'], 'contabilidad.csv');

    const event1 = { target: { files: [file1] } } as unknown as Event;
    const event2 = { target: { files: [file2] } } as unknown as Event;

    component.onFacturasChange(event1);
    component.onContabilidadChange(event2);

    expect(component.facturasFile).toBe(file1);
    expect(component.contabilidadFile).toBe(file2);
  });

  it('should call service and show result', () => {
    const file1 = new File(['content'], 'facturas.csv');
    const file2 = new File(['content'], 'contabilidad.csv');

    component.facturasFile = file1;
    component.contabilidadFile = file2;

    const mockResult = {
      resumen: { total_facturas: 1, correctas: 1, inconsistencias: 0 },
      detalles: [{ id_factura_linea: 'F001_L1', id_factura: 'F001', estado: 'Correcta', causas: [] }],
    };

    component.procesar();

    const req = httpMock.expectOne('/api/conciliacion');
    expect(req.request.method).toBe('POST');
    req.flush(mockResult);

    expect(component.resultado()).toEqual(mockResult);
    expect(component.loading()).toBe(false);
  });

  it('should show error when service fails', () => {
    const file1 = new File(['content'], 'facturas.csv');
    const file2 = new File(['content'], 'contabilidad.csv');

    component.facturasFile = file1;
    component.contabilidadFile = file2;

    component.procesar();

    const req = httpMock.expectOne('/api/conciliacion');
    req.flush({ detail: 'Error de servidor' }, { status: 500, statusText: 'Server Error' });

    expect(component.error()).toBe('Error de servidor');
    expect(component.loading()).toBe(false);
  });

  it('should filter detalles by estado', () => {
    component.resultado.set({
      resumen: { total_facturas: 3, correctas: 2, inconsistencias: 1 },
      detalles: [
        { id_factura_linea: 'F001_L1', id_factura: 'F001', estado: 'Correcta', causas: [] },
        { id_factura_linea: 'F002_L2', id_factura: 'F002', estado: 'Correcta', causas: [] },
        { id_factura_linea: 'F003_L3', id_factura: 'F003', estado: 'Con inconsistencia', causas: ['IVA incorrecto'] },
      ],
    });

    component.filtro.set('correctas');
    expect(component.detallesFiltrados().length).toBe(2);

    component.filtro.set('inconsistencias');
    expect(component.detallesFiltrados().length).toBe(1);

    component.filtro.set('todos');
    expect(component.detallesFiltrados().length).toBe(3);
  });
});
