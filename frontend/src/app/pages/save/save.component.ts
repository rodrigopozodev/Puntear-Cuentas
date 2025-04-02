import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FileService } from '../../services/file.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-save',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  template: `
    <div class="p-4">
      <div *ngIf="status" class="mt-4 p-4 rounded" [ngClass]="statusClass">
        {{ statusMessage }}
      </div>
    </div>
  `
})
export class SaveComponent {
  status: 'success' | 'error' | null = null;
  statusMessage = '';
  statusClass = '';
  private readonly PYTHON_API = 'http://localhost:3000/execute-python';

  constructor(
    private fileService: FileService,
    private http: HttpClient,
    private router: Router
  ) {}

  saveExcel(file: File) {
    this.fileService.saveExcelToFolder(file).subscribe({
      next: (response) => {
        this.status = 'success';
        this.statusMessage = 'Archivo guardado exitosamente';
        this.statusClass = 'bg-green-100 text-green-800';
        this.executePythonScript();
      },
      error: (error) => {
        this.status = 'error';
        this.statusMessage = 'Error al guardar el archivo';
        this.statusClass = 'bg-red-100 text-red-800';
        console.error('Error:', error);
      }
    });
  }

  private executePythonScript() {
    this.http.post(this.PYTHON_API, {}).subscribe({
      next: (response) => {
        console.log('Script Python ejecutado:', response);
        // Navegar a la página de informes después de que Python termine
        this.router.navigate(['/informes']);
      },
      error: (err) => console.error('Error ejecutando script Python:', err)
    });
  }
}