import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './component/home/home.component'
import { LoginComponent } from './component/login/login.component'
import { NavbarComponent } from './component/navbar/navbar.component'
import { AuthGaurdService } from './service/auth-gaurd.service';
import { LogoutComponent } from './component/logout/logout.component';
import { CropComponent } from './component/crop/crop.component';

export const AppRoutes: Routes = [
  { path: 'home', component: HomeComponent },  
  { path: 'login', component: LoginComponent },
  { path: 'crop', component: CropComponent},
  { path: 'logout', component: LogoutComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(AppRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
