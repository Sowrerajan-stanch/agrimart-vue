<template>
	<nav class="bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700">
		<div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
			<a href="#" class="flex items-center space-x-3 rtl:space-x-reverse">
				<span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white"
					>AgriMart</span
				>
			</a>
			<button
				data-collapse-toggle="navbar-dropdown"
				type="button"
				class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
				aria-controls="navbar-dropdown"
				aria-expanded="false"
			>
				<span class="sr-only">Open main menu</span>
				<svg
					class="w-5 h-5"
					aria-hidden="true"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 17 14"
				>
					<path
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M1 1h15M1 7h15M1 13h15"
					/>
				</svg>
			</button>
			<div class="hidden w-full md:block md:w-auto" id="navbar-dropdown" v-if="isUserLogged">
				<ul
					class="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
				>
					<li>
						<a
							href="/"
							class="block py-2 px-3 text-white rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500 dark:bg-blue-600 md:dark:bg-transparent"
							:class="{ 'text-bg-500': currentRouteName === 'Home' }"
							aria-current="page"
							>Home</a
						>
					</li>

					<li>
						<a
							href="/Products"
							class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
							>Products</a
						>
					</li>
					<li>
						<a
							href="/Cart"
							class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
							>Cart({{ getCartLength }})</a
						>
					</li>
					<li>
						<a
							href="#"
							class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
							>Orders</a
						>
					</li>
					<li>
						<a
							href="#"
							class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
							@click="signOut"
							>Sign out</a
						>
					</li>
				</ul>
			</div>
			<div class="hidden w-full md:block md:w-auto" id="navbar-dropdown" v-else>
				<ul
					class="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
				>
					<li>
						<a
							href="/Login"
							class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
							>Login</a
						>
					</li>
				</ul>
			</div>
		</div>
	</nav>
</template>
<script>
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import router from '../router'

const { isUserLogged, user } = storeToRefs(useUserStore())

export default {
	name: 'Navbar',
	data() {
		return {
			isUserLogged: isUserLogged,
		}
	},
	computed: {
		currentRouteName() {
			return this.$route.name
		},
		getCartLength() {
			const cartStore = useCartStore()
			const { cartLength } = storeToRefs(cartStore)

			return cartLength.value
		},
	},
	methods: {
		signOut() {
			axios
				.get('http://agri-app.localhost:80812/api/method/logout')
				.then((res) => {
					console.log(res)
					isUserLogged.value = false
					user.value = {
						username: '',
						email: '',
						address: '',
					}
					router.push({
						path: '/Login',
					})
				})
				.catch((err) => {
					console.log(err)
				})
		},
	},
}
</script>
