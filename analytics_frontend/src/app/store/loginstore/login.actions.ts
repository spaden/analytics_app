import { createAction, props } from "@ngrx/store";
import { Login } from "./login.model";
export const updateUserDetails = createAction('USER_DETAILS',
    props<{logindetails: any}>()
)
