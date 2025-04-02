import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private readonly API_URL = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  uploadExcel(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('excel', file);

    return this.http.post(`${this.API_URL}/upload`, formData, {
      reportProgress: true,
      observe: 'events'
    }).pipe(
      map(event => {
        switch (event.type) {
          case HttpEventType.UploadProgress:
            if (event.total) {
              const progress = Math.round(100 * event.loaded / event.total);
              return { progress };
            }
            return { progress: 0 };
          case HttpEventType.Response:
            return event.body;
          default:
            return `Evento no manejado: ${event.type}`;
        }
      })
    );
  }
}
