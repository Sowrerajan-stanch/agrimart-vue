<template>
	<Navbar></Navbar>
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
		<div
			v-for="product in products"
			:key="product.name"
			class="bg-white rounded-lg shadow-md overflow-hidden"
		>
			<div class="p-4">
				<h2 class="text-lg font-semibold text-gray-800">{{ product.product_name }}</h2>
				<p class="text-gray-600">{{ product.product_description }}</p>
				<div class="mt-4 flex justify-between items-center">
					<span class="text-gray-800 font-semibold"
						>Rs. {{ product.product_price }}</span
					>
				</div>
				<div class="flex items-center justify-between">
					<p>
						<span class="font-semibold text-gray-800">Farmer:</span>
						{{ product.farmer_name }}
					</p>
					<button
						class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
						@click.prevent="addToCart(product)"
					>
						Add to Cart
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import Navbar from '../components/Navbar.vue'
import { useCartStore } from '@/stores/cart'

export default {
	name: 'Products',
	data() {
		return {
			products: [],
		}
	},
	methods: {
		fetchProducts() {
			axios
				.get(
					'http://agri-app.localhost:8081/api/resource/Product?fields=["name","product_name","product_description","product_price","farmer_name"]'
				)
				.then((res) => {
					const productList = []
					res.data.data.forEach((product) => {
						productList.push({
							product_name: product['product_name'],
							product_description: product['product_description'],
							product_price: product['product_price'],
							farmer_name: product['farmer_name'],
							quantity: 0,
						})
					})
					this.products = productList
				})
				.catch((err) => {
					console.log(err)
				})
		},
		addToCart(product) {
			const cartStore = useCartStore()
			cartStore.addToCart(product)
		},
	},
	created() {
		this.fetchProducts()
	},
	components: {
		Navbar,
	},
}
</script>
