import { Injectable } from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {Observable} from 'rxjs'
import { Login } from 'src/app/store/loginstore/login.model'
import { Store } from '@ngrx/store'
import { UserData } from 'src/app/store/userdata/userdata.model'

@Injectable({
    providedIn: 'root'
})
export class FileUploadService {
	
    // API url
    baseApiUrl = "http://localhost:3004/fileupload"
    
    username: string = ''

    constructor(private http:HttpClient,
        private store: Store<{login: Login, userReportData: UserData}>) { 
        this.store.select(state => state.login).subscribe(res => {
            this.username = res.username
        })    
    }
    
    // Returns an observable
    upload(file: any):Observable<any> {
    
    	// Create form data
    	const formData = new FormData();
    		
    	// Store form name as "file" with file data
    	formData.append("myFile", file, file.name)

        formData.append('username', this.username)
    		
    	// Make http post request over api
    	// with formData as req
    	return this.http.post(this.baseApiUrl, formData)
    }
}
