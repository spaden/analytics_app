import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {

  @Input() name: string | any

  @Input() value: string | any
  
  @Input() placeholder: string | any

  @Input() type: string = 'text'

  @Output('onChange') updatedValue = new EventEmitter<{name: string, value: string}>()

  @ViewChild('inputElement') inputElement: ElementRef | any

  constructor() { }

  ngOnInit(): void {}

  onInputChange() {
    this.updatedValue.emit({name: this.name, value: this.inputElement.value})
  }
}
