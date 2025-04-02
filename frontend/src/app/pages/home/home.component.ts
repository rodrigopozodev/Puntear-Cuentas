import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { FileService } from '../../services/file.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './home.component.html'
})
export class HomeComponent {
  constructor(
    private router: Router,
    private fileService: FileService
  ) {}

  navegarAInformes() {
    this.router.navigate(['/informes']);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      if (this.isExcelFile(file)) {
        this.fileService.saveExcelToFolder(file).subscribe({
          next: () => {
            console.log('Archivo subido exitosamente');
            this.navegarAInformes();
          },
          error: (error) => {
            console.error('Error al subir el archivo:', error);
            alert('Error al subir el archivo');
          }
        });
      } else {
        alert('Por favor, selecciona un archivo Excel válido (.xlsx, .xls)');
      }
    }
  }

  private isExcelFile(file: File): boolean {
    return file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
           file.type === 'application/vnd.ms-excel';
  }
}