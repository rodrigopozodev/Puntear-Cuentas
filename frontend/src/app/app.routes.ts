import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { SaveComponent } from './pages/save/save.component';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'save', component: SaveComponent },
  {
    path: 'informes',
    loadComponent: () => import('./pages/informes/informes.component')
      .then(m => m.InformesComponent)
  },
  { path: '**', redirectTo: 'home' }
];
