import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AnalyticsComponent } from './views/analytics/analytics.component';
import { HomeComponent } from './views/home/home.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'analytics', component: AnalyticsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
