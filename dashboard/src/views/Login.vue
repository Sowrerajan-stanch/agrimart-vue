<template>
	<div class="min-h-screen min-w-screen bg-white flex items-center">
		<div class="mx-auto w-full max-w-sm lg:w-96">
			<h2 class="text-[2rem] font-bold mb-5 text-center">Login</h2>
			<form class="space-y-6 border p-10 rounded-md">
				<div class="flex flex-col gap-2">
					<label for="username">Username</label>
					<InputText
						id="username"
						class="border p-2"
						v-model="email"
						aria-describedby="username-help"
					/>
				</div>
				<br />
				<div class="flex flex-col gap-2">
					<label for="password">Password</label>
					<Password
						class="border p-2 focus:outline-none"
						v-model="password"
						toggleMask
					/>
				</div>

				<Button
					class="bg-blue-500 text-white px-[0.5rem] py-[0.25rem]"
					label="Submit"
					@click.prevent="login"
				/>
			</form>
		</div>
	</div>
</template>
<script>
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";

export default {
	name: "Login",
	data() {
		return {
			email: null,
			password: null,
		};
	},
	inject: ["$auth"],
	async mounted() {
		if (this.$route?.query?.route) {
			this.redirect_route = this.$route.query.route;
			this.$router.replace({ query: null });
		}
	},
	methods: {
		async login() {
			if (this.email && this.password) {
				let res = await this.$auth.login(this.email, this.password);
				if (res) {
					this.$router.push({ name: "Home" });
				}
			}
		},
	},
	components: {
		InputText,
		Password,
		Button,
	},
};
</script>
