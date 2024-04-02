<template>
	<div>
		<Navbar />
		<div class="p-5">
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
				<div
					v-for="product in productList"
					:key="product.name"
					class="bg-white rounded-lg shadow-md overflow-hidden"
				>
					<div class="p-4">
						<h2 class="text-lg font-semibold text-gray-800">
							{{ product.product_name }}
						</h2>
						<p class="text-gray-600">{{ product.product_description }}</p>
						<div class="mt-4 flex justify-between items-center">
							<span class="text-gray-800 font-semibold"
								>Price: Rs. {{ product.product_price }}</span
							>
						</div>
						<div class="flex items-center justify-between">
							<p>
								<span class="font-semibold text-gray-800">Farmer:</span>
								{{ product.farmer_name }}
							</p>
							<Button
								class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
								@click="showDialog(product)"
								label="Add to Cart"
							/>
						</div>
					</div>
				</div>
			</div>
		</div>

		<Dialog
			v-model:visible="dialogVisible"
			modal
			header="Product Info"
			:style="{ width: '25rem' }"
			@hide="closeDialog"
		>
			<div>
				<span class="p-text-secondary block mb-5">
					Product: {{ selectedProduct.product_name }}
				</span>
				<span class="p-text-secondary block mb-5">
					Description: {{ selectedProduct.product_description }}
				</span>
				<span class="p-text-secondary block mb-5">
					Price: Rs. {{ selectedProduct.product_price }}
				</span>
				<div class="flex items-center gap-3 mb-5">
					<label for="quantity" class="font-semibold w-6rem">Quantity:</label>
					<InputText
						id="quantity"
						v-model="quantity"
						class="flex-auto border p-2"
						autocomplete="off"
					/>
				</div>
				<div class="flex justify-end gap-2">
					<Button type="button" label="Cancel" severity="danger" @click="closeDialog" />
					<Button
						class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
						@click="addToCart"
						label="Add to Cart"
					/>
				</div>
			</div>
		</Dialog>
	</div>
</template>

<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";

export default {
	name: "Products",
	data() {
		return {
			productList: [],
			isLoading: false,
			dialogVisible: false,
			selectedProduct: {},
			quantity: 0,
		};
	},
	mounted() {
		this.fetchProducts();
	},
	methods: {
		async fetchProducts() {
			this.isLoading = true;
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.product.list_products"
				);
				this.productList = response.data.message || [];
			} catch (error) {
				console.error("Error fetching products:", error);
			} finally {
				this.isLoading = false;
			}
		},
		showDialog(product) {
			this.dialogVisible = true;
			this.selectedProduct = product;
			this.quantity = null;
		},
		closeDialog() {
			this.dialogVisible = false;
		},
		addToCart() {
			if (this.quantity == null || this.quantity <= 0) {
				alert("Enter some product quantity");
				return;
			}
			console.log(
				"Adding product to cart:",
				this.selectedProduct,
				"Quantity:",
				this.quantity
			);
			axios
				.post("http://agri-app.localhost:8080/api/method/agriapp.agriuser.add_to_cart", {
					user: "US0001",
					product_id: this.selectedProduct.name,
					quantity: this.quantity,
				})
				.then((response) => {
					if (response.data.message.error) {
						alert(response.data.message.error);
						this.dialogVisible = false;
					} else {
						alert(response.data.message.message);
						this.dialogVisible = false;
					}
				})
				.catch((err) => console.log(err));
		},
	},
	components: {
		Navbar,
		Button,
		Dialog,
		InputText,
	},
};
</script>
