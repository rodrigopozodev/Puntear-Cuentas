import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { SaveComponent } from '../save/save.component';
import { firstValueFrom } from 'rxjs';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, SaveComponent],
  templateUrl: './home.component.html'
})
export class HomeComponent {
  @ViewChild('saveComponent') saveComponent!: SaveComponent;

  constructor(private http: HttpClient) {}

  async clearReports() {
    const confirm = window.confirm('¿Estás seguro? Si vuelves a la página principal, todos los informes serán borrados de la vista actual. ¿Deseas continuar?');
    if (confirm) {
      try {
        await firstValueFrom(this.http.delete('https://puntear-cuentas.onrender.com/informes'));
        console.log('Informes borrados exitosamente');
      } catch (error) {
        console.error('Error al borrar informes:', error);
      }
    }
  }

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
