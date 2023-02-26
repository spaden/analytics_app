import { Component, OnInit, ViewChild } from '@angular/core';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';
import { FileUploadService } from 'src/app/services/fileupload.service';
import { UserData } from 'src/app/store/userdata/userdata.model';
import { Login } from 'src/app/store/loginstore/login.model'
import { Store } from '@ngrx/store'
import { updateUserReportDetails } from 'src/app/store/userdata/userdata.actions';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {
    
  pTestData: any = {}

  confi: Array<number> = []
  overallRatingCount: any

  postiveWords: any = []

  reviewData: any = []

  file: File | undefined

  isFileUploading: boolean = false

  data: any | undefined

  username: any
  
  constructor(private fileUploadService: FileUploadService,
    private store: Store<{login: Login, userReportData: UserData}>) {}

  
  checkIfDataExists() {
    return JSON.stringify(this.data) === '{}'
  }


  countRatingDataUtil() {
    let ctrating = JSON.parse(this.data.ratingOverYears.ctrating)

    let avrating = JSON.parse(this.data.ratingOverYears.rating)
    
    let labels = []
    let dt = []
    
    let keys = Object.keys(ctrating)
    let keysAv = Object.keys(avrating)


    labels = Object.values(ctrating[keys[0]])
    dt = Object.values(ctrating[keys[1]])
    
    let avLabels = Object.values(avrating[keysAv[0]])
    let dtav = Object.values(avrating[keysAv[1]])

    this.createChart('bar', labels,
      dt,
      'Rating count over years', 
      'testchart')

    this.createChart('bar', avLabels, dtav, 'Average rating over year', 'anchart')

  }


  createChart(charttype: any, labels: Array<any>, data: Array<any>, title: string, id: string,
    options: any = {}) {
    return new Chart(id, {
        type: charttype,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data
            }]
        },
        options: options
    })
  }

  createReviewUtil() {
    const reviewData = JSON.parse(this.data.orgSent)
    
    const modifiedData = []

    for (let reviewItem in reviewData) {
      modifiedData.push({
        name: reviewData[reviewItem].name,
        postDate: reviewData[reviewItem].reviewDate,
        reviewText: reviewData[reviewItem].reviewText,
        label: reviewData[reviewItem].predsentiment
      })
    }
    
    this.reviewData = modifiedData

  }

  ngOnInit(): void {
    
    this.store.select(state => state.userReportData).subscribe(res => {
      this.data = res
    })

    this.store.select(state => state.login).subscribe(res => {
      this.username = res.username
    })


    this.createChart('line', Object.keys(JSON.parse(this.data.ratDifferenceYears)),
        Object.values(JSON.parse(this.data.ratDifferenceYears)),
        'Rating Difference over years', 
        'diffchart')
    this.countRatingDataUtil()

    this.confi = Object.values(this.data.confidence_interval)

    this.pTestData = JSON.parse(this.data.ptests)

    this.overallRatingCount = JSON.parse(this.data.ratingCount)

    this.createChart('bar', Object.keys(this.overallRatingCount), Object.values(this.overallRatingCount),
      'Overall Rating count',
      'overallrat')


    this.createReviewUtil()
  }

  onFileChange(event: any) {
    this.file = event.target.files[0]
    console.log(this.file)
  }

  uploadFile() {
    this.isFileUploading = true
    this.fileUploadService.upload(this.file).subscribe(res => {
      this.store.dispatch(updateUserReportDetails({ userreportdetails: res.dt }))
      this.isFileUploading = false
    }, err => {
      this.isFileUploading = false
    })
  }

}
