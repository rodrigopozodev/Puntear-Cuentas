import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-save',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="p-4">
      <div *ngIf="status" class="mt-4 p-4 rounded" [ngClass]="statusClass">
        {{ statusMessage }}
        <div *ngIf="errorDetails" class="mt-2 text-sm">
          {{ errorDetails }}
        </div>
      </div>
    </div>
  `
})
export class SaveComponent {
  @Output() backToHome = new EventEmitter<void>();

  status: string | null = null;
  statusMessage: string = '';
  statusClass: string = '';
  errorDetails: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  saveExcel(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    this.status = 'uploading';
    this.statusMessage = 'Subiendo archivo...';
    this.statusClass = 'bg-blue-100 text-blue-800';
    this.errorDetails = '';

    this.http.post('http://localhost:3000/save-excel', formData)
      .subscribe({
        next: () => {
          this.executePythonScript();
        },
        error: (error: HttpErrorResponse) => {
          this.handleError('Error al guardar el archivo', error);
        }
      });
  }

  private executePythonScript() {
    this.status = 'processing';
    this.statusMessage = 'Procesando archivo...';
    this.statusClass = 'bg-blue-100 text-blue-800';

    this.http.post('http://localhost:3000/execute-python', {})
      .subscribe({
        next: (response: any) => {
          if (response.success) {
            this.status = 'success';
            this.statusMessage = 'Archivo procesado exitosamente';
            this.statusClass = 'bg-green-100 text-green-800';
            console.log('Python script output:', response.output);
            // Esperar un segundo antes de navegar para que el usuario vea el mensaje de éxito
            setTimeout(() => {
              this.router.navigate(['/informes']);
            }, 1000);
          } else {
            this.handleError('Error al procesar el archivo', {
              error: { message: response.output }
            } as HttpErrorResponse);
          }
        },
        error: (error: HttpErrorResponse) => {
          this.handleError('Error al procesar el archivo', error);
        }
      });
  }

  private handleError(message: string, error: HttpErrorResponse) {
    this.status = 'error';
    this.statusMessage = message;
    this.statusClass = 'bg-red-100 text-red-800';
    
    if (error.error?.details) {
      this.errorDetails = error.error.details;
    } else if (error.error?.message) {
      this.errorDetails = error.error.message;
    }
    
    console.error('Error:', error);
  }

  // Cuando el usuario navega de vuelta a home
  goBack() {
    this.backToHome.emit();
  }
}