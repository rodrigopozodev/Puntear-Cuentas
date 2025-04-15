import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { SaveComponent } from './pages/save/save.component';

export const routes: Routes = [
  { path: '', component: HomeComponent }, // Ruta raíz que carga el HomeComponent sin cambiar la URL
  { path: 'home', component: HomeComponent }, // Esta ruta puede ser innecesaria, ya que la raíz ya redirige a Home
  { path: 'save', component: SaveComponent },
  {
    path: 'informes',
    loadComponent: () => import('./pages/informes/informes.component')
      .then(m => m.InformesComponent)
  },
  { path: '**', redirectTo: '' } // Si hay una URL desconocida, redirige a la raíz
];
