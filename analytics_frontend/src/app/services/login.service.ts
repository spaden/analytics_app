import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Login } from '../store/loginstore/login.model';


@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private http: HttpClient) { }

  checkUser(data: Login) {
    return this.http.post('http://localhost:3000/user/checkuser', {
        username: data.username,
        userpass: data.password
    })
  }
}