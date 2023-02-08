import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputComponent } from './input/input.component';
import { ButtonComponent } from './button/button.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../material.module';
import { SpinnerComponent } from './spinner/spinner.component';



@NgModule({
  declarations: [
    InputComponent,
    ButtonComponent,
    SpinnerComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule
  ],
  exports: [
    InputComponent,
    ButtonComponent,
    SpinnerComponent
  ]
})
export class FormsModuleModule { }
