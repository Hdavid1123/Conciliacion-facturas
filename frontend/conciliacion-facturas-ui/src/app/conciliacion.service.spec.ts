import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { ConciliacionService } from './conciliacion.service';

describe('ConciliacionService', () => {
  let service: ConciliacionService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });
    service = TestBed.inject(ConciliacionService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should send POST request with files', () => {
    const file1 = new File(['content'], 'facturas.csv');
    const file2 = new File(['content'], 'contabilidad.csv');

    service.conciliar(file1, file2).subscribe();

    const req = httpMock.expectOne('/api/conciliacion');
    expect(req.request.method).toBe('POST');
    expect(req.request.body.get('facturas')).toBe(file1);
    expect(req.request.body.get('contabilidad')).toBe(file2);
  });
});
