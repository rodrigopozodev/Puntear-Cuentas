import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { InformesService, InformeFile, ExcelData } from '../../services/informes.service';
import { ScrollingModule } from '@angular/cdk/scrolling';

const informesPath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes';

@Component({
  selector: 'app-informes',
  standalone: true,
  imports: [CommonModule, HttpClientModule, ScrollingModule],
  templateUrl: './informes.component.html',
  styleUrls: ['./informes.component.css']
})
export class InformesComponent implements OnInit {
  informes: { [folder: string]: InformeFile[] } = {};
  selectedFile: InformeFile | null = null;
  excelData: ExcelData | null = null;
  loading = true;
  loadingData = false;
  error: string | null = null;
  showConfirmDialog = false;
  displayedRows: any[] = [];
  isLoadingTable = false;
  loadingFiles: { [key: string]: boolean } = {}; // Añade esta línea

  constructor(private informesService: InformesService) {}

  ngOnInit() {
    this.loadInformes();
  }

  loadInformes() {
    this.loading = true;
    this.informesService.getInformes().subscribe({
      next: (files) => {
        this.informes = files.reduce((acc, file) => {
          const folder = file.folder || 'Principal';
          if (!acc[folder]) {
            acc[folder] = [];
          }
          acc[folder].push(file);
          return acc;
        }, {} as { [folder: string]: InformeFile[] });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los informes';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  getFiles(): InformeFile[] {
    return Object.values(this.informes).flat();
  }

  hasInformes(): boolean {
    return Object.keys(this.informes).length > 0;
  }

  downloadInforme(file: InformeFile) {
    if (!file || !file.path) {
      this.error = 'Error: Archivo no válido';
      return;
    }

    this.informesService.downloadInforme(file.path).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = file.name;
        link.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error('Error al descargar:', err);
        this.error = 'Error al descargar el informe';
      }
    });
  }

  formatSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  }

  getInformeKeys(): string[] {
    return Object.keys(this.informes);
  }

  viewExcelContent(file: InformeFile) {
    if (!file || !file.path) {
      this.error = 'Error: Archivo no válido';
      return;
    }

    try {
      this.loadingFiles[file.path] = true;
      this.selectedFile = file;
      this.loadingData = true;
      this.isLoadingTable = true;
      this.error = null;
      
      this.informesService.getExcelContent(file.path).subscribe({
        next: (data) => {
          if (!data || !data.rows) {
            throw new Error('Datos no válidos');
          }
          
          this.excelData = data;
          this.displayedRows = data.rows;
          this.loadingData = false;
          this.loadingFiles[file.path] = false;
          
          requestAnimationFrame(() => {
            this.isLoadingTable = false;
          });
        },
        error: (err) => {
          console.error('Error al cargar datos:', err);
          this.error = this.getErrorMessage(err);
          this.loadingData = false;
          this.isLoadingTable = false;
          this.selectedFile = null;
          this.loadingFiles[file.path] = false;
        }
      });
    } catch (error) {
      console.error('Error inesperado:', error);
      this.error = 'Error inesperado al procesar el archivo';
      this.loadingFiles[file.path] = false;
    }
  }

  private getErrorMessage(error: any): string {
    if (error.status === 400) {
      return 'Error: La ruta del archivo no es válida o el archivo no es accesible';
    } else if (error.status === 404) {
      return 'Error: El archivo no fue encontrado';
    } else if (error.status === 500) {
      return 'Error del servidor al procesar el archivo';
    }
    return 'Error al cargar los datos del archivo';
  }

  closeModal() {
    this.selectedFile = null;
    this.excelData = null;
  }

  stopPropagation(event: Event) {
    event.stopPropagation();
  }

  showDialog() {
    this.showConfirmDialog = true;
  }

  hideDialog() {
    this.showConfirmDialog = false;
  }

  navigateToHome() {
    // Primero intentamos borrar la carpeta
    this.informesService.deleteInformesFolder().subscribe({
      next: () => {
        // Si se borra correctamente, limpiamos los datos y navegamos
        this.informes = {};
        this.selectedFile = null;
        this.excelData = null;
        this.displayedRows = [];
        this.error = null;
        
        // Redirigimos a la página principal
        window.location.href = 'http://localhost:4200/';
      },
      error: (err) => {
        console.error('Error al borrar la carpeta de informes:', err);
        this.error = 'Error al borrar los informes';
      }
    });
  }

  trackByIndex(index: number): number {
    return index;
  }
}
