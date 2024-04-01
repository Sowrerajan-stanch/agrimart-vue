<template>
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
						:type="'text'"
						variant="subtle"
						placeholder="Enter your Password"
						:disabled="false"
						label="Password"
						v-model="password"
					/>
				</div>
				<div class="flex justify-center mt-5">
					<button class="bg-[#383838] text-white w-full rounded-md text-sm py-[0.25rem]">
						Submit
					</button>
				</div>
			</form>
		</div>
	</div>
</template>
<script>
import { Input, createDocumentResource } from 'frappe-ui'
import Navbar from '../components/Navbar.vue'
export default {
	name: 'Signup',
	components: {
		Navbar,
		Input,
	},
}
</script>
