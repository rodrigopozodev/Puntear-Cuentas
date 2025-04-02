import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { SaveComponent } from './pages/save/save.component';
import { InformesComponent } from './pages/informes/informes.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'save', component: SaveComponent },
  { path: 'informes', component: InformesComponent },
  { path: '**', redirectTo: '' }
];
