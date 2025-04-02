import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FileService } from '../../services/file.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule
  ],
  providers: [FileService],
  templateUrl: './home.component.html'
})
export class HomeComponent {
  uploadProgress: number = 0;
  isUploading: boolean = false;
  
  constructor(private fileService: FileService) {}

  onFileSelected(event: Event): void {
    const element = event.target as HTMLInputElement;
    const file = element.files?.[0];
    
    if (file && this.isExcelFile(file)) {
      this.uploadFile(file);
    } else {
      alert('Por favor, selecciona un archivo Excel válido (.xlsx, .xls)');
    }
  }

  private uploadFile(file: File): void {
    this.isUploading = true;
    this.uploadProgress = 0;

    this.fileService.uploadExcel(file).subscribe({
      next: (response: any) => {
        if (response.progress) {
          this.uploadProgress = response.progress;
        } else {
          console.log('Archivo subido exitosamente:', response);
          this.isUploading = false;
          alert('Archivo subido con éxito');
        }
      },
      error: (error) => {
        console.error('Error al subir el archivo:', error);
        this.isUploading = false;
        alert('Error al subir el archivo');
      }
    });
  }

  private isExcelFile(file: File): boolean {
    return file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
           file.type === 'application/vnd.ms-excel';
  }
}