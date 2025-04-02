import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FileService } from '../../services/file.service';

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

  constructor(private fileService: FileService) {}

  saveExcel(file: File) {
    this.fileService.saveExcelToFolder(file).subscribe({
      next: (response) => {
        this.status = 'success';
        this.statusMessage = 'Archivo guardado exitosamente';
        this.statusClass = 'bg-green-100 text-green-800';
      },
      error: (error) => {
        this.status = 'error';
        this.statusMessage = 'Error al guardar el archivo';
        this.statusClass = 'bg-red-100 text-red-800';
        console.error('Error:', error);
      }
    });
  }
}