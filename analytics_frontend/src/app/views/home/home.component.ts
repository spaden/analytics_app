import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { LoginService } from 'src/app/services/login.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  
  @ViewChild('f') form: NgForm | any
  
  username = ''
  userpass = ''
  checkinguser: Boolean = false
  
  constructor(private http: HttpClient, private loginservice: LoginService) { }

  ngOnInit(): void {
  }
  

  onInputChange(event: any) {
    if (event.name == 'userpass') {
      this.userpass = event.value
    } else {
      this.username = event.value
    }
  }

  authUser() {
    this.checkinguser = true
    this.loginservice.checkUser({
      username: this.username,
      userpass: this.userpass
    }).subscribe(resp => {
      this.checkinguser = false
    }, error => {
      alert(error)
    })
  
  }
}
