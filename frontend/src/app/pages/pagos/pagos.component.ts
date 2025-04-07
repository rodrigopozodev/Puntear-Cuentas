import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-pagos',
  templateUrl: './pagos.component.html',
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class PagosComponent {
  selectedPaymentMethod: string = '';
  selectedPlan: any = null;
  
  plans = [
    {
      name: 'Básico',
      price: 9.99,
      features: ['Hasta 1000 registros', 'Soporte básico', 'Exportación PDF']
    },
    {
      name: 'Profesional',
      price: 19.99,
      features: ['Hasta 10000 registros', 'Soporte prioritario', 'Exportación múltiple', 'API access']
    },
    {
      name: 'Empresarial',
      price: 49.99,
      features: ['Registros ilimitados', 'Soporte 24/7', 'Todas las características', 'Multiple usuarios']
    }
  ];

  selectPlan(plan: any) {
    this.selectedPlan = plan;
    this.selectedPaymentMethod = '';
  }

  selectPaymentMethod(method: string) {
    this.selectedPaymentMethod = method;
  }

  processCreditCardPayment(formData: any) {
    console.log('Procesando pago con tarjeta:', formData);
    // Implementar lógica de pago con tarjeta
  }

  processPayPalPayment() {
    console.log('Iniciando pago con PayPal');
    // Implementar lógica de PayPal
  }

  processBizumPayment(phone: string) {
    console.log('Procesando pago con Bizum:', phone);
    // Implementar lógica de Bizum
  }
}