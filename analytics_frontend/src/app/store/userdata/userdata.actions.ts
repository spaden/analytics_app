import { createAction, props } from "@ngrx/store"
import { UserData } from "./userdata.model"

export const updateUserReportDetails = createAction('USER_REPORT_DETAILS',
    props<{userreportdetails: any}>()
)
