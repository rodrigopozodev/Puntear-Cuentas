import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { InformesService } from '../../services/informes.service';

@Component({
  selector: 'app-informes',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './informes.component.html'
})
export class InformesComponent implements OnInit {
  informes: string[] = [];
  loading = true;
  error: string | null = null;
  private checkInterval: any;

  constructor(
    private informesService: InformesService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadInformes();
    // Verificar nuevos informes cada 2 segundos
    this.checkInterval = setInterval(() => this.checkNewInformes(), 2000);
  }

  ngOnDestroy() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
  }

  loadInformes() {
    this.loading = true;
    this.error = null;

    this.informesService.getInformes().subscribe({
      next: (files) => {
        this.informes = files;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los informes';
        this.loading = false;
        console.error('Error:', err);
      }
    });
  }

  checkNewInformes() {
    this.informesService.getInformes().subscribe({
      next: (files) => {
        if (files.length > this.informes.length) {
          this.informes = files;
          // Navegar a la página de informes si hay nuevos
          this.router.navigate(['/informes']);
        }
      }
    });
  }

  downloadInforme(filename: string) {
    this.informesService.downloadInforme(filename).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error('Error al descargar:', err);
        alert('Error al descargar el informe');
      }
    });
  }

  getFileDate(filename: string): Date {
    // Extraer la fecha del nombre del archivo si tiene un formato específico
    // Por ahora devuelve la fecha actual
    return new Date();
  }
}