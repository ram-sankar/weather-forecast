import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface DataResponse {  
  api : string;
  date : string;
  description : string;
  humidity : string;
  max_temp : string;
  min_temp : string;
  next : {
    date : string;
    description : string;
    temp : string;
  }
  pressure : string;
  city : string;
}

interface CropResponse{
  list :{
    description : string;
    name : string;
    weather : string;
  }
}

@Injectable({
  providedIn: 'root'
})
export class FetchdataService {

  baseUrl = "http://localhost:5000/";
  url="";
  constructor(private http : HttpClient) { }

  getCityData(cityName)
  {
    this.url = this.baseUrl + "";
    return this.http.post<DataResponse>(this.url, { "city":cityName} );
  }
  getCropData(cityName)
  {
    this.url = this.baseUrl + "crop";
    return this.http.post<CropResponse>(this.url, { "city":cityName} );
  }
}
