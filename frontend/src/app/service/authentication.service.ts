import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface UserResponse {  
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService 
{
    baseUrl = "http://localhost:5000/";
    url="";
    constructor(private http : HttpClient) { }

    addNewUser(email, username, phone, password)
    {
        this.url = this.baseUrl + "auth/signup";
        return this.http.post(this.url, { "email":email, "username":username, "phoneno":phone, "password":password} );        
    }

    authenticate(mailid, password) 
    {    
        this.url = this.baseUrl + "auth/login";
        return this.http.post<UserResponse>(this.url, { "email":mailid,"password":password} );        
        //return this.http.post<UserResponse>(this.url, { "username":mailid,"password":password} );        
    }

    isUserLoggedIn() {
    let user = sessionStorage.getItem('username')
    return !(user === null)
    }

    logOut() {
    sessionStorage.removeItem('username')
    }
 
}
