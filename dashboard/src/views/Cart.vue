<template>
	<div>
		<Navbar />
		<div class="p-5">
			<div v-if="cartItems.length === 0" class="text-center text-gray-600 mt-8">
				Your cart is empty
			</div>
			<div v-else>
				<div
					v-for="(item, index) in cartItems"
					:key="index"
					class="flex items-center border-b border-gray-200 pb-4 mb-4"
				>
					<div class="flex-grow">
						<h3 class="text-lg font-semibold">{{ item.ordered_product_name }}</h3>
						<div class="flex items-center mt-2">
							<span class="text-gray-700 font-semibold"
								>Price: Rs.{{ item.ordered_product_price }}</span
							>
							<div class="flex items-center ml-auto">
								<Button
									class="mr-2"
									icon="pi pi-minus"
									@click="decrementQuantity(index)"
								/>
								<InputText
									class="mr-2 p-2 w-[50px] text-center"
									readonly
									v-model="item.ordred_quanity"
								/>
								<Button
									class="mr-2"
									icon="pi pi-plus"
									@click="incrementQuantity(index)"
								/>
								<InputText
									class="mr-2 p-2 w-[80px] text-center"
									readonly
									:value="'Rs.' + calculateTotalPrice(item)"
								/>

								<Button icon="pi pi-trash" @click="removeFromCart(item)" />
							</div>
						</div>
					</div>
				</div>
				<div class="flex flex-col items-end justify-end">
					<p><span class="font-semibold">Total :</span> Rs. {{ calculateTotal() }}</p>
					<Button
						class="px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600"
						:label="isUpdatedQuantity ? 'Update quantity?' : 'Checkout'"
						@click.prevent="isUpdatedQuantity ? updateQuantity() : checkout()"
					/>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue";
import Button from "primevue/button";
import InputText from "primevue/inputtext";

export default {
	name: "Cart",
	data() {
		return {
			cartItems: [],
			isUpdatedQuantity: false,
		};
	},
	mounted() {
		this.list_cart_products();
	},
	computed: {
		calculateTotalPrice() {
			return (item) => {
				return parseInt(item.ordred_quanity) * parseInt(item.ordered_product_price);
			};
		},
	},
	methods: {
		async removeFromCart(item) {
			await axios
				.post(
					"http://agri-app.localhost:8080/api/method/agriapp.agriuser.remove_cart_item",
					{
						user: "US0001",
						product_id: item.name,
					}
				)
				.then((res) => {
					location.reload();
					console.log(res);
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async list_cart_products() {
			const cart_items = await axios.get(
				"http://agri-app.localhost:8080/api/method/agriapp.agriuser.fetch_cart?user=US0001"
			);
			this.cartItems = cart_items.data.message;
			console.log(this.cartItems);
		},
		incrementQuantity(index) {
			this.cartItems[index].ordred_quanity++;
			this.isUpdatedQuantity = true;
		},
		decrementQuantity(index) {
			if (this.cartItems[index].ordred_quanity > 1) {
				this.cartItems[index].ordred_quanity--;
				this.isUpdatedQuantity = true;
			}
		},
		calculateTotal() {
			return this.cartItems.reduce((total, item) => {
				return (
					total + parseInt(item.ordred_quanity) * parseInt(item.ordered_product_price)
				);
			}, 0);
		},
		async updateQuantity() {
			await axios
				.post(
					"http://agri-app.localhost:8080/api/method/agriapp.agriuser.update_quantity",
					{
						user: "US0001",
						cart: this.cartItems,
					}
				)
				.then((res) => {
					alert(res.data.message.message);
					this.isUpdatedQuantity = false;
					console.log(res);
				})
				.catch((err) => console.log(err));
		},
		async checkout() {
			await axios
				.post("http://agri-app.localhost:8080/api/method/agriapp.agriuser.pay_products", {
					user: "US0001",
					total_amount: this.calculateTotal(),
				})
				.then((res) => {
					alert("Checkout completed!");
					console.log(res);
					window.location.reload();
				})
				.catch((err) => console.log(err));
		},
	},
	components: {
		Navbar,
		Button,
		InputText,
	},
};
</script>
