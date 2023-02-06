import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthtokenService {

  constructor(private http: HttpClient) { }

  getToken() {
    return this.http.get('http://localhost:3000/authtoken', {observe: 'response'})
  }
}
