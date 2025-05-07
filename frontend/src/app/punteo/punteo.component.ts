import { Component, OnInit } from '@angular/core';
import axios from 'axios';

interface ResponseData {
  mensaje: string;
}

@Component({
  selector: 'app-punteo',
  templateUrl: './punteo.component.html',
  styleUrls: ['./punteo.component.css']
})
export class PunteoComponent implements OnInit {
  archivo: File | null = null;
  mensaje: string = "";

  ngOnInit() {
    // Ya no se llama a procesar() aquí para evitar la ejecución automática al iniciar el componente
  }

  seleccionarArchivo(event: Event) {
    const input = event.target as HTMLInputElement;
    this.archivo = input.files?.[0] || null;
  }

  async subir() {
    if (!this.archivo) return;

    const formData = new FormData();
    formData.append("file", this.archivo);

    try {
      const res = await axios.post<ResponseData>("http://localhost:8000/subir", formData);
      this.mensaje = res.data.mensaje;
    } catch (err: any) {
      this.mensaje = "Error subiendo archivo";
    }
  }

  async procesar() {
    try {
      // Primero, asegúrate de que el archivo haya sido subido
      const res = await axios.get<ResponseData>("http://localhost:8000/procesar");
      this.mensaje = res.data.mensaje;
    } catch (err: any) {
      this.mensaje = "Error procesando archivo";
    }
  }
}
