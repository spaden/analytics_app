import { HttpClient } from '@angular/common/http'
import { Component, OnInit, ViewChild } from '@angular/core'
import { NgForm } from '@angular/forms'
import { LoginService } from 'src/app/services/login.service'
import { Router } from '@angular/router'
import { Observable } from 'rxjs'
import { Store } from '@ngrx/store'
import { Login } from 'src/app/store/loginstore/login.model'
import { UserData } from 'src/app/store/userdata/userdata.model'
import { updateUserDetails } from 'src/app/store/loginstore/login.actions'
import { updateUserReportDetails } from 'src/app/store/userdata/userdata.actions'

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
              private store: Store<{login: Login, userReportData: UserData}>) { }

  ngOnInit(): void {
    this.loginDet = this.store.select(state => state.login)

    this.loginDet.subscribe(resp => {
      this.state.username = resp.username
      this.state.password = resp.password
    })
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
      let dt = {}
      // @ts-expect-error: Let's ignore a compile error like this unreachable code
      if(resp.length > 0) dt = resp[0]['userdata']
      this.store.dispatch(updateUserReportDetails({ userreportdetails: dt  }))

      setTimeout(() => {
        this.router.navigate(['/analytics'])
      }, 500)
    }, error => {
      this.userAuthError = true
      this.checkinguser = false
    })
  }
}
