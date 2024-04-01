import { defineStore } from "pinia"
export const useUserStore =  defineStore("user",{
	state:() => ({
		isUserLogged:false,
		user:{
			username:"",
			email:"",
			address:""
		}
	}),
	persist:true
})