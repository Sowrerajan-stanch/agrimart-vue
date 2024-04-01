<template>
	<Navbar />
	<div class="w-full h-[calc(100vh-60px)] flex items-center justify-center">
		<div class="p-10 border rounded">
			<form action="" class="">
				<div class="p-2">
					<Input
						:type="'text'"
						variant="subtle"
						placeholder="Enter your Email Address"
						:disabled="false"
						label="Email"
						v-model="email"
					/>
				</div>
				<div class="p-2">
					<Input
						:type="'password'"
						variant="subtle"
						placeholder="Enter your Password"
						:disabled="false"
						label="Password"
						v-model="password"
					/>
				</div>
				<div class="flex justify-center mt-5">
					<button
						class="bg-[#383838] text-white w-full rounded-md text-sm py-[0.25rem]"
						@click.prevent="authenticate_user"
					>
						Submit
					</button>
				</div>
			</form>
		</div>
	</div>
</template>
<script>
import Navbar from '../components/Navbar.vue'
import axios from 'axios'
import { Input } from 'frappe-ui'
import { useUserStore } from '@/stores/user'
import router from '../router'
import { storeToRefs } from 'pinia'

const { isUserLogged, user } = storeToRefs(useUserStore())

export default {
	name: 'Login',
	data() {
		return {
			email: '',
			password: '',
			remember_me: false,
		}
	},
	methods: {
		authenticate_user() {
			if (!this.email || !this.password) {
				return
			}
			axios
				.post('http://agri-app.localhost:8081/api/method/login', {
					usr: this.email,
					pwd: this.password,
				})
				.then((response) => {
					console.log(response)
					isUserLogged.value = true
					user.value = {
						username: response.data.full_name,
						email: this.email,
						location: 'Banglore',
					}
					router.push({
						path: '/',
					})
				})
				.catch((err) => console.log('error', err))
		},
	},
	components: {
		Navbar,
		Input,
	},
}
</script>
