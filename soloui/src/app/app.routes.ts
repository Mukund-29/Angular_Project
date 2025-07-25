import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HomeComponent } from './dashboard/home/home.component';
import { AutomationsComponent } from './dashboard/automations/automations.component';
import { DocumentationComponent } from './dashboard/documentation/documentation.component';
import { ProfileMenuComponent } from './dashboard/profile-menu/profile-menu.component';
import { BillEstimateCompareComponent } from './dashboard/automations/bill-estimate-compare/bill-estimate-compare.component';
import { authGuard } from './shared/guards/auth.guard';

export const routes: Routes = [
  { path: '', component: LoginComponent },

{
  path: 'dashboard',
  component: DashboardComponent,
  canActivate: [authGuard],
  children: [
    { path: '', component: HomeComponent },
    { path: 'home', component: HomeComponent },
    {
      path: 'automations',
      children: [
        { path: '', component: AutomationsComponent },
        { path: 'bill-estimate-compare', component: BillEstimateCompareComponent }
      ]
    },
    { path: 'documentation', component: DocumentationComponent },
    { path: 'profile', component: ProfileMenuComponent }
  ]
},

  { path: '**', redirectTo: '' },
];
