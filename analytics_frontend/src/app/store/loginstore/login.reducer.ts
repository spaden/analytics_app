import {  createReducer, on } from "@ngrx/store"
import { updateUserDetails } from "./login.actions"
import { Login } from "./login.model"

const initialState: Login = {
    username: '',
    password: ''
}

export const loginDetailsReducer = createReducer(
    initialState,
    on(updateUserDetails, (state: any, {logindetails} )=> {
        
        return logindetails
    })
)
