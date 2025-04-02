import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { SaveComponent } from '../save/save.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, HttpClientModule, SaveComponent],
  template: `
    <div class="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-5xl font-bold text-white mb-8">Gestor de Archivos Excel</h1>
        
        <input
          type="file"
          id="fileInput"
          accept=".xlsx,.xls"
          class="hidden"
          (change)="onFileSelected($event)"
          #fileInput>
            
        <button 
          (click)="fileInput.click()"
          class="bg-white text-purple-600 px-8 py-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 font-semibold text-lg">
          <span class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Subir Excel
          </span>
        </button>

        <app-save #saveComponent></app-save>
      </div>
    </div>
  `
})
export class HomeComponent {
  @ViewChild('saveComponent') saveComponent!: SaveComponent;

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      if (this.isExcelFile(file)) {
        this.saveComponent.saveExcel(file);
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