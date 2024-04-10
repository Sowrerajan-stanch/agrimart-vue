<template>
	<VendorNavBar />
	<div class="min-h-screen bg-gray-100 py-6">
		<div class="max-w-4xl mx-auto px-4">
			<h1 class="text-2xl font-semibold text-gray-800 mb-6">Buyers</h1>

			<!-- Buyers Table -->
			<div class="bg-white shadow-md rounded-md overflow-x-auto">
				<table class="min-w-full">
					<thead class="bg-gray-200">
						<tr>
							<th class="px-4 py-2">Username</th>
							<th class="px-4 py-2">Ordered Date</th>
							<th class="px-4 py-2">Product Name</th>
							<th class="px-4 py-2">Price</th>
							<th class="px-4 py-2">Quantity</th>
							<th class="px-4 py-2">Amount</th>
							<th class="px-4 py-2">Status</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(order, index) in paginatedOrders" :key="index">
							<td class="px-4 py-2">{{ order.username }}</td>
							<td class="px-4 py-2">{{ order.ordered_date }}</td>
							<td class="px-4 py-2">{{ order.product_name }}</td>
							<td class="px-4 py-2">{{ order.product_price }}</td>
							<td class="px-4 py-2">{{ order.quantity }}</td>
							<td class="px-4 py-2">{{ order.amount }}</td>
							<td class="px-4 py-2">{{ order.status }}</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div class="mt-4">
				<button
					class="px-4 py-2 bg-gray-200 rounded-md mr-2"
					@click="prevPage"
					:disabled="currentPage === 1"
				>
					Prev
				</button>
				<button
					class="px-4 py-2 bg-gray-200 rounded-md"
					@click="nextPage"
					:disabled="currentPage === pageCount"
				>
					Next
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import VendorNavBar from "../../components/Vendor/VendorNavBar.vue";
import axios from "axios";

export default {
	name: "Buyers",
	data() {
		return {
			orders: [],
			currentPage: 1,
			perPage: 10,
		};
	},
	methods: {
		async getSellingProducts() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.get_selling_products?farmer=FR0001"
				);
				this.orders = response.data.message.buyers;
			} catch (error) {
				console.error("Error fetching selling products:", error);
			}
		},
		prevPage() {
			if (this.currentPage > 1) {
				this.currentPage--;
			}
		},
		nextPage() {
			if (this.currentPage < this.pageCount) {
				this.currentPage++;
			}
		},
	},
	computed: {
		paginatedOrders() {
			const startIndex = (this.currentPage - 1) * this.perPage;
			const endIndex = startIndex + this.perPage;
			return this.orders.slice(startIndex, endIndex);
		},
		pageCount() {
			return Math.ceil(this.orders.length / this.perPage);
		},
	},
	mounted() {
		this.getSellingProducts();
	},
	components: {
		VendorNavBar,
	},
};
</script>
