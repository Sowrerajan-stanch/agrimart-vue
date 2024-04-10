<template>
	<div class="min-h-screen bg-gray-100">
		<Navbar />
		<div class="max-w-7xl mx-auto px-4 py-8">
			<h1 class="text-2xl font-semibold text-gray-800 mb-6">List of Orders</h1>
			<div v-if="orders.length === 0" class="text-gray-600 text-center">
				No orders found.
			</div>
			<div v-else>
				<div
					v-for="order in orders"
					:key="order.order_id"
					class="bg-white shadow-md rounded-md mb-4"
				>
					<div class="p-4 cursor-pointer" @click="showOrderDetails(order)">
						<div class="flex items-center justify-between">
							<h2 class="text-lg font-semibold">Order ID: {{ order.order_id }}</h2>
							<span class="text-sm text-gray-600"
								>Ordered Date: {{ order.ordered_date }}</span
							>
						</div>
						<div class="mt-2">
							<div class="flex items-center mb-2">
								<i class="pi pi-money-bill text-lg text-gray-600"></i>
								<span class="ml-2">Total Amount: Rs.{{ order.total_amount }}</span>
							</div>
							<div class="flex items-center">
								<i class="pi pi-check-circle text-lg text-gray-600"></i>
								<span class="ml-2">Status: {{ order.status }}</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<Dialog
			v-model:visible="dialogVisible"
			modal
			header="Order Details"
			:style="{ width: '800px' }"
		>
			<div v-if="selectedOrder">
				<h2>
					<span class="text-lg font-semibold mb-4">Order id:</span>
					<span class=""> {{ selectedOrder.order_id }}</span>
				</h2>
				<h2>
					<span class="text-lg font-semibold mb-4">Ordered Date:</span>
					<span class=""> {{ selectedOrder.ordered_date }}</span>
				</h2>
				<table class="table-auto w-full">
					<thead>
						<tr>
							<th class="border px-4 py-2">Product Name</th>
							<th class="border px-4 py-2">Price</th>
							<th class="border px-4 py-2">Quantity</th>
							<th class="border px-4 py-2">Total Amount</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(item, index) in selectedOrder.products" :key="index + 1">
							<td class="border px-4 py-2">{{ item.product_name }}</td>
							<td class="border px-4 py-2">{{ item.product_price }}</td>
							<td class="border px-4 py-2">{{ item.quantity }}</td>
							<td class="border px-4 py-2">{{ item.product_total_amount }}</td>
						</tr>
					</tbody>
				</table>
				<div class="mt-5">
					<h2>
						<span class="text-lg font-semibold mb-4">Total Amount:</span>
						<span class=""> Rs.{{ selectedOrder.total_amount }}</span>
					</h2>
					<h2>
						<span class="text-lg font-semibold mb-4">Status: </span>
						<span class="text-green-500"> {{ selectedOrder.status }}</span>
					</h2>
				</div>
				<div class="flex items-center justify-end">
					<Button
						@click="generatePdf"
						label="Download invoice"
						class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
					/>
				</div>
			</div>
		</Dialog>
	</div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import axios from "axios";
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";

pdfMake.vfs = pdfFonts.pdfMake.vfs;

export default {
	name: "Orders",
	data() {
		return {
			orders: [],
			dialogVisible: false,
			selectedOrder: null,
			heading: "Stanch.IO",
		};
	},
	mounted() {
		this.fetchOrders();
	},
	methods: {
		async fetchOrders() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.agriuser.fetch_orders?user=US0001"
				);
				this.orders = response.data.message;
				console.log(this.orders);
			} catch (error) {
				console.error("Error fetching orders:", error);
			}
		},
		generatePdf() {
			const invoiceData = {
				name: this.selectedOrder.name,
				orders: this.selectedOrder,
			};

			const dd = {
				pageSize: "B4",
				content: [
					{ text: "Stanch.io", style: "header" },
					{ text: "Bangalore, Karnataka", style: "subheader" },
					{ text: `Name : ${invoiceData.name}`, style: "info" },
					{ text: "Orders Info:", style: "subheader" },
					{
						table: {
							headerRows: 1,
							body: [
								[
									"Order ID",
									"Ordered Date",
									"Product Name",
									"Price",
									"Quantity",
									"Total Amount",
								],
								...invoiceData.orders.products.map((product) => [
									invoiceData.orders.order_id,
									invoiceData.orders.ordered_date,
									product.product_name,
									product.product_price,
									product.quantity,
									product.product_total_amount,
								]),
							],
						},
					},
					{ text: `Total Amount: Rs.${invoiceData.orders.total_amount}`, style: "info" },
					{ text: `Status: ${invoiceData.orders.status}`, style: "info" },
				],
				styles: {
					header: {
						fontSize: 22,
						bold: true,
						margin: [0, 0, 0, 10],
					},
					subheader: {
						fontSize: 18,
						bold: true,
						margin: [0, 10, 0, 5],
					},
					info: {
						margin: [0, 0, 0, 5],
					},
				},
			};

			const pdf = pdfMake.createPdf(dd);
			pdf.open();
		},
		showOrderDetails(order) {
			this.selectedOrder = order;
			this.dialogVisible = true;
		},
	},
	components: {
		Navbar,
		Dialog,
		Button,
	},
};
</script>
