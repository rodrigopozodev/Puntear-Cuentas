import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { InformesService, InformeFile } from '../../services/informes.service';

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
Object: any;

  constructor(private informesService: InformesService) {}

  ngOnInit() {
    this.loadInformes();
  }

  loadInformes() {
    this.loading = true;
    this.informesService.getInformes().subscribe({
      next: (files) => {
        // Agrupar archivos por carpeta
        this.informes = files.reduce((acc, file) => {
          if (!acc[file.folder]) {
            acc[file.folder] = [];
          }
          acc[file.folder].push(file);
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

  // Add this function to handle key iteration in the template
  getInformeKeys(): string[] {
    return Object.keys(this.informes);
  }
}
