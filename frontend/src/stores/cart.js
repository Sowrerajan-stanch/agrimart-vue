import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
	state: () => ({
		items: [],
	}),
	getters: {
		cartLength(state) {
			return state.items.length
		},
		getItemQuantity: (state) => (index) => {
			return state.items[index].quantity
		},
	},

	actions: {
		addToCart(item) {
			this.items.push(item)
		},
		removeFromCart(index) {
			this.items.splice(index, 1)
		},
		clearCart() {
			this.items = []
		},
		incrementQuantity(index) {
			this.items[index].quantity += 1
		},
		decrementQuantity(index) {
			if (this.items[index].quantity <= 0) {
				return
			}
			this.items[index].quantity -= 1
		},
	},
	persist: true,
})
