<template>
	<AdminNav />
	<div class="p-5">
		<h3 class="text-[2rem] font-semibold mb-2">Farmers</h3>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
			<div
				v-for="(farmer, index) in farmers"
				:key="index"
				class="bg-white rounded-lg shadow-md overflow-hidden"
			>
				<div class="p-4">
					<div class="text-center">
						<div class="flex items-center justify-center">
							<div class="pi pi-user"></div>
							<h3 class="text-lg font-semibold mb-2">{{ farmer.username }}</h3>
						</div>
						<p class="text-gray-600">{{ farmer.email }}</p>
					</div>
					<div class="flex justify-center mt-4">
						<Button
							label="View Details"
							class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
							@click.prevent="fetchParticularFarmerAnalytics(farmer.name, farmer)"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
	<Dialog v-model:visible="showDialog" header="Farmer analytics" @hide="hideDialog">
		<div class="p-5" v-if="currentFarmer && farmerAnalytics">
			<h3>
				<span class="text-lg font-semibold mb-2">Full name:</span>
				{{ currentFarmer.full_name }}
			</h3>
			<p>
				<span class="text-lg font-semibold mb-2">Email: </span>
				<span class="text-gray-600"> {{ currentFarmer.email }}</span>
			</p>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
				<div v-for="(value, key) in farmerAnalytics" :key="key">
					<div
						v-if="key !== 'products_count'"
						class="bg-white rounded-lg shadow-md overflow-hidden"
					>
						<div class="p-4">
							<h3 class="text-lg font-semibold mb-2">{{ key }}</h3>
							<p class="text-gray-600">{{ value }}</p>
						</div>
					</div>
				</div>
			</div>
			<div class="mt-5">
				<h3>
					<span class="text-lg font-semibold mb-2">Products Sold</span>
				</h3>
				<DataTable :value="productCountItems" showGridlines>
					<Column field="product" header="Product"></Column>
					<Column field="count" header="Count"></Column>
				</DataTable>
			</div>
		</div>
		<div class="flex items-center justify-end gap-5" v-if="currentFarmer && farmerAnalytics">
			<Button
				class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:bg-green-600"
				label="Download Excel"
				icon="pi pi-download"
				@click.prevent="downloadExcel"
			/>
			<JsonCSV :data="formattedData" :name="csvFileName">
				<Button
					class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
					label="Download CSV"
					icon="pi pi-download"
				/>
			</JsonCSV>
		</div>
	</Dialog>
</template>

<script>
import axios from "axios";
import AdminNav from "../../components/Admin/AdminNav.vue";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import JsonCSV from "vue-json-csv";
import * as XLSX from "xlsx";

export default {
	name: "FarmerReports",
	components: {
		AdminNav,
		Button,
		Dialog,
		DataTable,
		Column,
		JsonCSV,
	},
	data() {
		return {
			farmers: [],
			showDialog: false,
			farmerAnalytics: null,
			currentFarmer: null,
		};
	},
	methods: {
		async fetchFarmers() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmers_analytics"
				);
				this.farmers = response.data.message.farmers;
			} catch (error) {
				console.error("Error fetching farmers:", error);
			}
		},
		async fetchParticularFarmerAnalytics(farmerId, farmer) {
			try {
				const response = await axios.get(
					`http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_analytics?farmer=${farmerId}`
				);
				console.log(response.data.message);
				this.farmerAnalytics = response.data.message;
				this.currentFarmer = farmer;
				this.showDialog = true;
			} catch (err) {
				console.log(err);
			}
		},
		hideDialog() {
			this.showDialog = false;
			this.currentFarmer = null;
			this.farmerAnalytics = null;
		},
		downloadExcel() {
			const productCountData = this.farmerAnalytics.products_count;
			console.log(this.farmerAnalytics);
			const data = [
				[
					"Full Name",
					"Email",
					"Total Orders",
					"Total Revenue",
					"Orders Sold",
					"Highest Buying User",
					"Most Ordered Product",
					"Total Products Purchased",
				],
				[
					this.currentFarmer.full_name,
					this.currentFarmer.email,
					this.farmerAnalytics.total_orders,
					this.farmerAnalytics.total_revenue,
					this.farmerAnalytics.orders_sold,
					this.farmerAnalytics.highest_buying_user,
					this.farmerAnalytics.most_ordered_product,
					this.farmerAnalytics.total_products_purchased,
				],
			];

			for (const [product, count] of Object.entries(productCountData)) {
				data[0].push(product);
				data[1].push(count);
			}

			const workbook = XLSX.utils.book_new();
			const worksheet = XLSX.utils.aoa_to_sheet(data);
			XLSX.utils.book_append_sheet(workbook, worksheet, "Farmer Analytics");

			const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
			const excelData = new Blob([excelBuffer], {
				type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			});

			const link = document.createElement("a");
			link.href = window.URL.createObjectURL(excelData);
			link.setAttribute(
				"download",
				`farmer-analytics-${this.currentFarmer.username.replace(/\s+/g, "-")}.xlsx`
			);
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		},
	},
	computed: {
		productCountItems() {
			return Object.entries(this.farmerAnalytics.products_count).map(([product, count]) => ({
				product,
				count,
			}));
		},
		formattedData() {
			const productCountData = this.farmerAnalytics.products_count;
			const formattedData = [];
			const userData = {
				"Full Name": this.currentFarmer.full_name,
				Email: this.currentFarmer.email,
				"Total Orders": this.farmerAnalytics.total_orders,
				"Total Revenue": this.farmerAnalytics.total_revenue,
				"Orders Sold": this.farmerAnalytics.orders_sold,
				"Highest Buying User": this.farmerAnalytics.highest_buying_user,
				"Most Ordered Product": this.farmerAnalytics.most_ordered_product,
				"Total Products Purchased": this.farmerAnalytics.total_products_purchased,
			};
			formattedData.push(userData);
			for (const [product, count] of Object.entries(productCountData)) {
				userData[`${product}`] = count;
			}
			return formattedData;
		},
		csvFileName() {
			if (this.currentFarmer) {
				return `farmer-analytics-${this.currentFarmer.username.replace(/\s+/g, "-")}.csv`;
			}
			return "farmer-analytics.csv";
		},
	},
	mounted() {
		this.fetchFarmers();
	},
};
</script>
