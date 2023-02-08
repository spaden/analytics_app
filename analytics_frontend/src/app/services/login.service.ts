import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

interface userlogin {
    username: string
    userpass: string
}

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private http: HttpClient) { }

  checkUser(data: userlogin) {
    return this.http.post('http://localhost:3000/user/checkuser', {
        username: data.username,
        userpass: data.userpass
    })
  }
}