import { HttpClient } from '@angular/common/http'
import { Component, OnInit, ViewChild } from '@angular/core'
import { NgForm } from '@angular/forms'
import { LoginService } from 'src/app/services/login.service'
import { Router } from '@angular/router'
import { Observable } from 'rxjs'
import { Store } from '@ngrx/store'
import { Login } from 'src/app/store/loginstore/login.model'
import { updateUserDetails } from 'src/app/store/loginstore/login.actions'


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  
  @ViewChild('f') form: NgForm | any
  
  username: string = ''
  userpass: string = ''

  state: Login = {
    'username': '',
    'password': ''
  }
  checkinguser: Boolean = false
  userAuthError: Boolean = false

  loginDet: Observable<Login> | undefined
  
  constructor(private http: HttpClient, 
              private loginservice: LoginService, 
              private router: Router, 
              private store: Store<{login: Login}>) { }

  ngOnInit(): void {
    this.loginDet = this.store.select(state => this.state = state.login)
  }
  

  onInputChange(event: any) {
    let logindetails: Login = {
      ...this.state
    }

    if (event.name == 'userpass') {
      logindetails.password = event.value
    } else {
      logindetails.username = event.value
    }    
    this.store.dispatch(updateUserDetails({ logindetails }))
  }

  authUser() {
    this.checkinguser = true
    this.loginservice.checkUser(this.state).subscribe(resp => {
      this.checkinguser = false
      setTimeout(() => {
        this.router.navigate(['/analytics'])
      }, 2000)
    }, error => {
      this.userAuthError = true
      this.checkinguser = false
    })
  }
}
