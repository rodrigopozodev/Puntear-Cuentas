import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

export interface InformeFile {
  name: string;
  path: string;
  folder: string;
  size: number;
  createdAt: Date;
}

export interface ExcelData {
  headers: string[];
  rows: any[];
}

@Injectable({
  providedIn: 'root'
})
export class InformesService {
  private readonly API_URL = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  getInformes(): Observable<InformeFile[]> {
    console.log('Solicitando informes...');
    return this.http.get<InformeFile[]>(`${this.API_URL}/informes`).pipe(
      tap(files => console.log('Informes recibidos:', files)),
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

  getExcelContent(path: string): Observable<ExcelData> {
    return this.http.get<ExcelData>(`${this.API_URL}/informes/content`, {
      params: { path }
    });
  }

  deleteInformesFolder() {
    return this.http.delete(`${this.API_URL}/delete-informes-folder`);
  }
}