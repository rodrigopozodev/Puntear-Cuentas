import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { InformesService, InformeFile, ExcelData } from '../../services/informes.service';

const informesPath = 'C:/Users/rodri/Desktop/Mis Proyectos/Puntear Cuentas/informes';

@Component({
  selector: 'app-informes',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './informes.component.html',
  styleUrls: ['./informes.component.css']  // Añade esta línea
})
export class InformesComponent implements OnInit {
  informes: { [folder: string]: InformeFile[] } = {};
  selectedFile: InformeFile | null = null;
  excelData: ExcelData | null = null;
  loading = true;
  loadingData = false; // Añadida esta propiedad
  error: string | null = null;

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

    this.selectedFile = file;
    this.loadingData = true;
    this.error = null; // Limpiamos errores anteriores
    
    this.informesService.getExcelContent(file.path).subscribe({
      next: (data) => {
        this.excelData = data;
        this.loadingData = false;
      },
      error: (err) => {
        console.error('Error al cargar datos:', err);
        this.error = 'Error al cargar los datos del archivo';
        this.loadingData = false;
        this.selectedFile = null;
      }
    });
  }

  closeModal() {
    this.selectedFile = null;
    this.excelData = null;
  }

  stopPropagation(event: Event) {
    event.stopPropagation();
  }
}
