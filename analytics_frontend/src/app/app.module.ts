import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModuleModule } from './forms-module/forms-module.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthInterceptorService } from './services/authinterceptor.service';
import { HttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { HomeComponent } from './views/home/home.component';
import { AnalyticsComponent } from './views/analytics/analytics.component'
import { TagCloudComponent } from 'angular-tag-cloud-module';
import { StoreModule } from '@ngrx/store';
import { loginDetailsReducer } from './store/loginstore/login.reducer';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AnalyticsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    FormsModuleModule,
    BrowserAnimationsModule,
    HttpClientModule,
    TagCloudComponent,
    StoreModule.forRoot({
      login: loginDetailsReducer
    })
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
