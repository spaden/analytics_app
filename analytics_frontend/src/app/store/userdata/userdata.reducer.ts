import {  createReducer, on } from "@ngrx/store"
import { UserData } from "./userdata.model"
import { updateUserReportDetails } from "./userdata.actions"

const initialState: UserData = {
    confidence_interval: [],
    orgSent: [],
    ptest: {},
    ratDifferenceYears: {},
    ratingCount: {},
    ratingOverYears: {},
    wordCloud: {}
}

export const loginDetailsReducer = createReducer(
    initialState,
    on(updateUserReportDetails, (state: any, {userreportdetails} )=> {        
        return userreportdetails
    })
)
