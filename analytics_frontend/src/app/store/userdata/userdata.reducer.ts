import {  createReducer, on } from "@ngrx/store"
import { UserData } from "./userdata.model"
import { updateUserReportDetails } from "./userdata.actions"

const initialState: UserData = {
   userReportData: {}
}

export const userReportReducer = createReducer(
    initialState,
    on(updateUserReportDetails, (state: any, {userreportdetails} )=> {  
        console.log(userreportdetails)      
        return userreportdetails
    })
)
