import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpClient } from '@angular/common/http'
import { Injectable, Injector } from '@angular/core'
import { map, Observable, switchMap } from 'rxjs'
import { AuthtokenService } from './authtoken.service'

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {
	
	constructor(private injector: Injector) {}

	intercept(req: HttpRequest<any>, next: HttpHandler) {
		

		if (req.url == 'http://localhost:3000/login') {
            let http: HttpClient = this.injector.get(HttpClient);

            return http.get('http://localhost:3000/authtoken').pipe(switchMap((response: any) => {
				let clone: HttpRequest<any> = req.clone({ setHeaders: { 'auth-token': response['value'] } })
                
				// alert('Silent Call ready. Doing original call with Mocky headers');
                return next.handle(clone);
            }));
        } else {
            return next.handle(req);
        }
	}
}
