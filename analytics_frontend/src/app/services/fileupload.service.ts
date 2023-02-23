import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class FileUploadService {
	
    // API url
    baseApiUrl = "http://localhost:3004/fileupload"
    	
    constructor(private http:HttpClient) { }
    
    // Returns an observable
    upload(file: any):Observable<any> {
    
    	// Create form data
    	const formData = new FormData();
    		
    	// Store form name as "file" with file data
    	formData.append("myFile", file, file.name)

        formData.append('username', 'testuser')
    		
    	// Make http post request over api
    	// with formData as req
    	return this.http.post(this.baseApiUrl, formData)
    }
}
