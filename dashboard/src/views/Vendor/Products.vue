<template>
	<VendorNavbar />
	<div class="min-h-screen bg-gray-100 py-6">
		<div class="max-w-4xl mx-auto px-4">
			<h1 class="text-2xl font-semibold text-gray-800 mb-6">Selling Products</h1>

			<div class="bg-white shadow-md rounded-md p-6">
				<!-- Product Form -->
				<div class="mb-4">
					<label for="product-name" class="block text-sm font-medium text-gray-700"
						>Product Name</label
					>
					<InputText
						v-model="productName"
						id="product-name"
						class="mt-1 w-full p-2 border"
					/>
				</div>

				<div class="mb-4">
					<label
						for="product-description"
						class="block text-sm font-medium text-gray-700"
						>Product Description</label
					>
					<InputText
						v-model="productDescription"
						id="product-description"
						class="mt-1 w-full p-2 border"
					/>
				</div>

				<div class="mb-4">
					<label for="product-price" class="block text-sm font-medium text-gray-700"
						>Product Price</label
					>
					<InputText
						v-model="productPrice"
						id="product-price"
						class="mt-1 w-full p-2 border"
					/>
				</div>

				<div class="flex justify-end">
					<Button
						@click.prevent="addProduct"
						class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
					>
						Add Product
					</Button>
				</div>
			</div>

			<!-- Selling Products Table -->
			<div class="mt-8">
				<h2 class="text-xl font-semibold mb-4">Selling Products</h2>
				<div class="bg-white shadow-md rounded-md overflow-x-auto">
					<table class="min-w-full">
						<thead class="bg-gray-200">
							<tr>
								<th class="px-4 py-2">Product Name</th>
								<th class="px-4 py-2">Description</th>
								<th class="px-4 py-2">Price</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="product in products" :key="product.product_id">
								<td class="px-4 py-2">{{ product.product_name }}</td>
								<td class="px-4 py-2">{{ product.product_desc }}</td>
								<td class="px-4 py-2">{{ product.product_price }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import VendorNavbar from "../../components/Vendor/VendorNavBar.vue";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import axios from "axios";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

export default {
	name: "VendorProducts",
	data() {
		return {
			productName: null,
			productDescription: null,
			productPrice: null,
			products: [],
		};
	},
	methods: {
		async addProduct() {
			await axios
				.post("http://agri-app.localhost:8080/api/method/agriapp.farmer.add_product", {
					product_name: this.productName,
					product_description: this.productDescription,
					product_price: this.productPrice,
					farmer: "FR0001",
				})
				.then((res) => {
					if (res.data) {
						alert("Product Created Successfully!");
						console.log(res.data);
						this.productName = null;
						this.productDescription = null;
						this.productPrice = null;
						location.reload();
					}
				})
				.catch((err) => {
					console.log(err);
				});
		},
		async getSellingProducts() {
			await axios
				.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.get_selling_products?farmer=FR0001"
				)
				.then((res) => {
					this.products = res.data.message.selling_products;
				})
				.catch((err) => {
					console.log(err);
				});
		},
	},
	mounted() {
		this.getSellingProducts();
	},
	components: {
		VendorNavbar,
		InputText,
		Button,
	},
};
</script>
