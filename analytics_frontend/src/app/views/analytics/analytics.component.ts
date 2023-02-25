import { Component, OnInit, ViewChild } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { data } from '../../utils/sampledata'
Chart.register(...registerables);
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';
import { FileUploadService } from 'src/app/services/fileupload.service';

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
  
  constructor(private fileUploadService: FileUploadService) {}


  countRatingDataUtil() {
    let ctrating = JSON.parse(data.ratingOverYears.ctrating)

    let avrating = JSON.parse(data.ratingOverYears.rating)
    
    let labels = []
    let dt = []
    
    let keys = Object.keys(ctrating)
    let keysAv = Object.keys(avrating)


    labels = Object.values(ctrating[keys[0]])
    dt = Object.values(ctrating[keys[1]])
    
    let avLabels = Object.values(avrating[keysAv[0]])
    let dtav = Object.values(avrating[keysAv[1]])

    var test = this.createChart('bar', labels,
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
    const reviewData = JSON.parse(data.orgSent)
    
    const modifiedData = []

    for (let reviewItem in reviewData) {

      modifiedData.push({
        name: reviewData[reviewItem][0],
        postDate: reviewData[reviewItem][6],
        reviewText: reviewData[reviewItem][7],
        label: reviewData[reviewItem][12]
      })
    }
    
    this.reviewData = modifiedData

    console.log(this.reviewData)
  }

  ngOnInit(): void {
    this.createChart('line', Object.keys(JSON.parse(data.ratDifferenceYears)),
        Object.values(JSON.parse(data.ratDifferenceYears)),
        'Rating Difference over years', 
        'diffchart')
    this.countRatingDataUtil()

    this.confi = Object.values(data.confidence_interval)

    this.pTestData = JSON.parse(data.ptests)

    this.overallRatingCount = JSON.parse(data.ratingCount)

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
      alert('uploaded')
      this.isFileUploading = false
    }, err => {
      alert(err)
      this.isFileUploading = false
    })
  }

}
