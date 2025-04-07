import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { SaveComponent } from './pages/save/save.component';

export const routes: Routes = [
  { path: '', redirectTo: 'pagos', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'save', component: SaveComponent },
  {
    path: 'informes',
    loadComponent: () => import('./pages/informes/informes.component')
      .then(m => m.InformesComponent)
  },
  {
    path: 'pagos',
    loadComponent: () => import('./pages/pagos/pagos.component')
      .then(m => m.PagosComponent)
  },
  { path: '**', redirectTo: 'pagos' }
];
