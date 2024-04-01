<template>
	<Navbar></Navbar>
	<div class="p-5">
		<h2 class="text-2xl font-semibold mb-4">Shopping Cart</h2>
		<div v-if="cartItems.length === 0" class="text-gray-600">Your cart is empty.</div>
		<div v-else>
			<div
				v-for="(item, index) in cartItems"
				:key="index"
				class="flex items-center justify-between border-b pb-2 mb-2"
			>
				<div class="flex items-center space-x-4">
					<div>
						<h3 class="font-semibold">{{ item.product_name }}</h3>
						<p class="text-gray-600">{{ item.product_price }}</p>
					</div>
				</div>
				<div class="flex items-center space-x-2">
					<button
						@click="decrementQuantity(index)"
						class="px-2 py-1 bg-gray-200 text-gray-700 rounded"
					>
						-
					</button>
					<input
						type="text"
						v-model.number="cartItems[index].quantity"
						class="w-12 text-center"
						readonly
						min="1"
					/>
					<button
						@click="incrementQuantity(index)"
						class="px-2 py-1 bg-gray-200 text-gray-700 rounded"
					>
						+
					</button>
					<button @click="removeFromCart(index)" class="text-red-500">Remove</button>
				</div>
			</div>
			<div class="flex justify-end">
				<button
					@click="pay"
					class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
				>
					Pay
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { useCartStore } from '@/stores/cart'
import Navbar from '../components/Navbar.vue'
export default {
	name: 'Cart',
	computed: {
		cartItems() {
			return useCartStore().items
		},
	},
	methods: {
		incrementQuantity(index) {
			const cartStore = useCartStore()
			cartStore.incrementQuantity(index)
		},
		decrementQuantity(index) {
			const cartStore = useCartStore()
			cartStore.decrementQuantity(index)
		},
		removeFromCart(index) {
			const cartStore = useCartStore()
			cartStore.removeFromCart(index)
		},
		pay() {
			console.log('Payment processing...')
		},
	},
	components: {
		Navbar,
	},
}
</script>
