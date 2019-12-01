import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../../service/authentication.service'

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(private loginService:AuthenticationService) { }

  ngOnInit() {
  }
  getUsername(){
    return sessionStorage.getItem('username');
    //return 'Ram Sankar R';
  }
}
