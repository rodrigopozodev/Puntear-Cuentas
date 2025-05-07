import { bootstrapApplication } from '@angular/platform-browser';
import { PunteoComponent } from './app/punteo/punteo.component';
import { appConfig } from './app/app.config';

bootstrapApplication(PunteoComponent, appConfig)
  .catch((err) => console.error(err));
