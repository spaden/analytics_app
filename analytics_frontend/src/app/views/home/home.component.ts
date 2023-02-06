import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  
  @ViewChild('f') form: NgForm | any
  
  username = ''
  userpass = ''
  
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
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
