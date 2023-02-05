import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent implements OnInit {
  
  @Input() name: string | any

  @Input() disabled: boolean | any

  @Input() value: string | any

  @Input() btnType: string | any
  
  @Output() onClick = new EventEmitter<{name: string}>()

  constructor() { }

  ngOnInit(): void {
  }

  onClicked() {
    this.onClick.emit({name: this.name})
  }

}
