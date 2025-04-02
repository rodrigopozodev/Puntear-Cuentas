import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InformesService {
  private readonly API_URL = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  getInformes(): Observable<string[]> {
    return this.http.get<string[]>(`${this.API_URL}/informes`);
  }

  downloadInforme(filename: string): Observable<Blob> {
    return this.http.get(`${this.API_URL}/informes/${filename}`, {
      responseType: 'blob'
    });
  }
}