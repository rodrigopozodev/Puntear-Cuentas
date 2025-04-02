import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface InformeFile {
  name: string;
  path: string;
  folder: string;
  size: number;
  createdAt: Date;
}

@Injectable({
  providedIn: 'root'
})
export class InformesService {
  private readonly API_URL = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  getInformes(): Observable<InformeFile[]> {
    return this.http.get<InformeFile[]>(`${this.API_URL}/informes`).pipe(
      map(files => files.map(file => ({
        ...file,
        createdAt: new Date(file.createdAt)
      })))
    );
  }

  downloadInforme(path: string): Observable<Blob> {
    return this.http.get(`${this.API_URL}/informes/download`, {
      params: { path },
      responseType: 'blob'
    });
  }
}