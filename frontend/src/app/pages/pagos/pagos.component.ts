import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-pagos',
  templateUrl: './pagos.component.html',
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class PagosComponent {
  selectedPaymentMethod: string = '';
  selectedPlan: any = null;
  showFreePlan: boolean = true;
  expirationDate = new Date('2025-04-13');

  ngOnInit() {
    this.checkFreePlanAvailability();
  }

  private checkFreePlanAvailability() {
    const now = new Date();
    this.showFreePlan = now < this.expirationDate;
  }
  
  plans = [
    {
      name: 'Plan Gratuito',
      price: 0,
      features: ['Ventaja 1', 'Ventaja 2', 'Ventaja 3']
    },
    {
      name: 'Plan Estándar',
      price: 3.99,
      features: ['Ventaja 1', 'Ventaja 2', 'Ventaja 3']
    },
    {
      name: 'Plan Premium',
      price: 9.99,
      features: ['Ventaja 1', 'Ventaja 2', 'Ventaja 3']
    }
  ];

  constructor(private router: Router) {}

  selectPlan(plan: any) {
    if (plan.noPayment) {
      // Plan gratuito
      this.router.navigate(['/home']);
    } else {
      this.selectedPlan = plan;
      this.selectedPaymentMethod = '';
    }
  }

  selectPaymentMethod(method: string) {
    this.selectedPaymentMethod = method;
  }

  processCreditCardPayment(formData: any) {
    console.log('Procesando pago con tarjeta:', formData);
    this.router.navigate(['/home']);
  }

  processPayPalPayment() {
    console.log('Iniciando pago con PayPal');
    this.router.navigate(['/home']);
  }

  processBizumPayment(phone: string) {
    console.log('Procesando pago con Bizum:', phone);
    this.router.navigate(['/home']);
  }
}