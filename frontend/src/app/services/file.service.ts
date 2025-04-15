import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private readonly SAVE_PATH = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/data';
  private readonly API_URL = 'https://puntear-cuentas.onrender.com';

  constructor(private http: HttpClient) {}

  saveExcelToFolder(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('savePath', this.SAVE_PATH);

    return this.http.post(`${this.API_URL}/save-excel`, formData);
  }
}