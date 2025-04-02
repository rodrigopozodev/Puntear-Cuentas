import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { InformesService, InformeFile, ExcelData } from '../../services/informes.service';

@Component({
  selector: 'app-informes',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './informes.component.html'
})
export class InformesComponent implements OnInit {
  informes: { [folder: string]: InformeFile[] } = {};
  loading = true;
  error: string | null = null;
  selectedFile: InformeFile | null = null;
  excelData: ExcelData | null = null;
  loadingData = false;

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

  hasInformes(): boolean {
    return Object.keys(this.informes || {}).length > 0;
  }

  downloadInforme(file: InformeFile) {
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
        alert('Error al descargar el informe');
      }
    });
  }

  formatSize(bytes: number): string {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${parseFloat((bytes / Math.pow(1024, i)).toFixed(2))} ${sizes[i]}`;
  }

  getInformeKeys(): string[] {
    return Object.keys(this.informes);
  }

  viewExcelContent(file: InformeFile) {
    this.selectedFile = file;
    this.loadingData = true;
    this.informesService.getExcelContent(file.path).subscribe({
      next: (data) => {
        this.excelData = data;
        this.loadingData = false;
      },
      error: (err) => {
        console.error('Error al cargar datos:', err);
        this.loadingData = false;
      }
    });
  }

  closeModal() {
    this.selectedFile = null;
    this.excelData = null;
  }
}
