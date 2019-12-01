import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faCloud } from '@fortawesome/free-solid-svg-icons';
import { FetchdataService } from '../../service/fetchdata.service';
 
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  celcius ;
  kelvin;
  temp;
  api;
  description = '';
  humidity = '';
  max_temp = '';
  min_temp = '';
  cityFetch = '';
  pressure = '';
  upcomingCelcius = {};



  constructor(private router: Router,private dataservice: FetchdataService) {  }

  ngOnInit() 
  {
    this.getDataCity("chennai");
  }

  getDataCity(cityName)
  {
    this.dataservice.getCityData(cityName)
    .subscribe(
      data => {
        this.cityFetch = data.city;
        this.max_temp = data.max_temp;
        this.min_temp = data.min_temp;
        this.kelvin = (parseInt(this.max_temp)+parseInt(this.min_temp))/2;
        this.celcius = this.kelvin - 273;
        this.celcius = this.celcius.toFixed(0);
        this.description = data.description;
        this.humidity = data.humidity;
        this.upcomingCelcius = data.next;
        this.api = data.api;
        this.pressure = data.pressure;
        console.log(this.celcius)
      },
      error => {
        console.log(error);
      }
    )
  }
  faCloud = faCloud;

}
