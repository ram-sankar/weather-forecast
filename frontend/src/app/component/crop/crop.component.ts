import { Component, OnInit } from '@angular/core';
import { FetchdataService } from '../../service/fetchdata.service';

@Component({
  selector: 'app-crop',
  templateUrl: './crop.component.html',
  styleUrls: ['./crop.component.css']
})
export class CropComponent implements OnInit {

  cropList = {};
  cityN='';
  constructor(private dataservice: FetchdataService) {  }

  ngOnInit() 
  {
    this.getCropCity("theni");
  }

  getCropCity(cityName)
  {
    this.cityN = cityName;
    this.dataservice.getCropData(cityName)
    .subscribe(
      data => {
        this.cropList = data.list;
        console.log(data);
      },
      error => {
        console.log(error);
      }
    )
  }

}
