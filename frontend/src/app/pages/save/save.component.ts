import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpEventType } from '@angular/common/http';

@Component({
  selector: 'app-save',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './save.component.html'
})
export class SaveComponent {
  selectedFile: File | null = null;
  uploadProgress: number = 0;
  uploadStatus: 'idle' | 'uploading' | 'success' | 'error' = 'idle';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file && this.isExcelFile(file)) {
      this.selectedFile = file;
      this.uploadStatus = 'idle';
    } else {
      alert('Por favor, seleccione un archivo Excel válido (.xlsx, .xls)');
    }
  }

  isExcelFile(file: File): boolean {
    return file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
           file.type === 'application/vnd.ms-excel';
  }

  uploadFile() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.uploadStatus = 'uploading';
    
    this.http.post('http://localhost:3000/upload', formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round(100 * event.loaded / event.total);
        }
        if (event.type === HttpEventType.Response) {
          this.uploadStatus = 'success';
        }
      },
      error: (error) => {
        console.error('Error al subir el archivo:', error);
        this.uploadStatus = 'error';
      }
    });
  }
}