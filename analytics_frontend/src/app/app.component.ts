import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  @ViewChild('f') form: NgForm | any
  
  username = ''
  userpass = ''

  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    console.log(this.form)
  }

  onInputChange(event: any) {
    if (event.name == 'userpass') {
      this.userpass = event.value
    } else {
      this.username = event.value
    }
  }

  test() {
    this.http.post('http://localhost:3000/login', {
      username: this.username,
      userpass: this.userpass
    }).subscribe(response => {
      console.log(response)
    })
  }
    
}
