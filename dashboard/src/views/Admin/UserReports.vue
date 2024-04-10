<template>
	<AdminNav />
	<div class="p-5">
		<div class="flex items-center justify-between">
			<h3 class="text-[2rem] font-semibold mb-2">Users</h3>
			<div class="relative">
				<p>Search</p>
				<input
					type="text"
					v-model="searchValue"
					class="border p-2 focus:outline-none"
					@input="handleInputChange"
					@click="showSuggestions = true"
				/>
				<div
					v-if="showSuggestions"
					class="w-[500px] border rounded absolute right-28 p-10 bg-white z-10"
				>
					<p class="cursor-pointer" @click="showSuggestions = false">X</p>
					<div
						v-for="suggestion in filteredSuggestions"
						:key="suggestion"
						@click="selectSuggestion(suggestion)"
						class="cursor-pointer p-2 hover:bg-gray-300"
					>
						<p class="font-bold">{{ suggestion.userId }}</p>
						<div class="flex items-center gap-5 flex-wrap">
							<p>{{ suggestion.full_name }}</p>
							<p>{{ suggestion.email }}</p>
						</div>
					</div>
					<div v-if="filteredSuggestions.length == 0">No Users Found!</div>
				</div>
			</div>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
			<div v-if="filteredUsers.length == 0">
				<p>No Users found</p>
			</div>
			<div
				v-else
				v-for="(user, index) in filteredUsers"
				:key="index"
				class="bg-white rounded-lg shadow-md overflow-hidden"
			>
				<div class="p-4">
					<div class="text-center">
						<div class="flex items-center justify-center">
							<div class="pi pi-user"></div>
							<h3 class="text-lg font-semibold mb-2">{{ user.full_name }}</h3>
						</div>
						<p class="text-gray-600">{{ user.email }}</p>
					</div>
					<div class="flex justify-center mt-4">
						<Button
							label="View Details"
							class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
							@click.prevent="fetchParticularUserAnalytics(user.name, user)"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
	<Dialog v-model:visible="showDialog" header="User Analytics" @hide="hideDialog">
		<div class="p-5" v-if="currentUser && userAnalytics">
			<h3>
				<span class="text-lg font-semibold mb-2">Full name:</span>
				{{ currentUser.full_name }}
			</h3>
			<p>
				<span class="text-lg font-semibold mb-2">Email: </span>
				<span class="text-gray-600"> {{ currentUser.email }}</span>
			</p>
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
				<div v-for="(value, key) in userAnalytics" :key="key">
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
					<span class="text-lg font-semibold mb-2">Products Brought</span>
				</h3>
				<DataTable :value="productCountItems" showGridlines>
					<Column field="product" header="Product"></Column>
					<Column field="count" header="Count"></Column>
				</DataTable>
			</div>
		</div>
		<div class="flex items-center justify-end gap-5" v-if="currentUser && userAnalytics">
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
import Listbox from "primevue/listbox";
import { debounce } from "lodash";

export default {
	name: "UserReports",
	components: {
		AdminNav,
		Button,
		Dialog,
		DataTable,
		Column,
		JsonCSV,
		Listbox,
	},
	data() {
		return {
			users: [],
			showDialog: false,
			userAnalytics: null,
			currentUser: null,
			searchValue: null,
			showSuggestions: false,
		};
	},
	methods: {
		async fetchUsers() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.agriuser.users_analytics"
				);
				this.users = response.data.message.users;
			} catch (error) {
				console.error("Error fetching users:", error);
			}
		},
		async fetchParticularUserAnalytics(userId, user) {
			try {
				const response = await axios.get(
					`http://agri-app.localhost:8080/api/method/agriapp.agriuser.user_analytics?user=${userId}`
				);
				this.userAnalytics = response.data.message;
				this.currentUser = user;
				this.showDialog = true;
			} catch (err) {
				console.log(err);
			}
		},
		hideDialog() {
			this.showDialog = false;
			this.currentUser = null;
			this.userAnalytics = null;
		},
		downloadExcel() {
			const productCountData = this.userAnalytics.products_count;

			const data = [
				[
					"Full Name",
					"Email",
					"Total Orders",
					"Total Spent",
					"Most Ordered Product",
					"Average Order Value",
					"Total Products Purchased",
				],
				[
					this.currentUser.full_name,
					this.currentUser.email,
					this.userAnalytics.total_orders,
					this.userAnalytics.total_spent,
					this.userAnalytics.most_ordered_product,
					this.userAnalytics.average_order_value,
					this.userAnalytics.total_products_purchased,
				],
			];

			for (const [product, count] of Object.entries(productCountData)) {
				data[0].push(product);
				data[1].push(count);
			}

			const workbook = XLSX.utils.book_new();
			const worksheet = XLSX.utils.aoa_to_sheet(data);
			XLSX.utils.book_append_sheet(workbook, worksheet, "User Analytics");

			const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
			const excelData = new Blob([excelBuffer], {
				type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			});

			const link = document.createElement("a");
			link.href = window.URL.createObjectURL(excelData);
			link.setAttribute(
				"download",
				`user-analytics-${this.currentUser.full_name.replace(/\s+/g, "-")}.xlsx`
			);
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		},
		handleInputChange() {
			if (this.searchValue) {
				this.showSuggestions = true;
			} else {
				this.showSuggestions = false;
			}
		},

		selectSuggestion(suggestion) {
			this.searchValue = suggestion.userId;
			this.showSuggestions = false;
		},
		handleInputChange: debounce(function () {
			this.showSuggestions = this.searchValue.trim() !== "";
		}, 300),
	},
	computed: {
		filteredUserIds() {
			return this.users.map((user) => user.name);
		},
		filteredSuggestions() {
			// Filter based on start value
			const startsWithFilter = this.users
				.map((user) => {
					return {
						userId: user.name,
						full_name: user.full_name,
						email: user.email,
					};
				})
				.filter(
					(user) =>
						user.userId.toLowerCase().startsWith(this.searchValue.toLowerCase()) ||
						user.full_name.toLowerCase().startsWith(this.searchValue.toLowerCase()) ||
						user.email.toLowerCase().startsWith(this.searchValue.toLowerCase())
				);

			// Filter based on end value
			const endsWithFilter = this.users
				.map((user) => {
					return {
						userId: user.name,
						full_name: user.full_name,
						email: user.email,
					};
				})
				.filter(
					(user) =>
						user.userId.toLowerCase().endsWith(this.searchValue.toLowerCase()) ||
						user.full_name.toLowerCase().endsWith(this.searchValue.toLowerCase()) ||
						user.email.toLowerCase().endsWith(this.searchValue.toLowerCase())
				);

			// Filter based on search key
			const includesFilter = this.users
				.map((user) => {
					return {
						userId: user.name,
						full_name: user.full_name,
						email: user.email,
					};
				})
				.filter(
					(user) =>
						user.userId.toLowerCase().includes(this.searchValue.toLowerCase()) ||
						user.full_name.toLowerCase().includes(this.searchValue.toLowerCase()) ||
						user.email.toLowerCase().includes(this.searchValue.toLowerCase())
				);

			return startsWithFilter.length
				? startsWithFilter
				: endsWithFilter.length
				? endsWithFilter
				: includesFilter;
		},
		filteredUsers() {
			if (!this.searchValue) {
				return this.users;
			} else {
				const suggestedUserIds = this.filteredSuggestions.map((user) =>
					user.userId.toLowerCase()
				);
				return this.users.filter((user) =>
					suggestedUserIds.includes(user.name.toLowerCase())
				);
			}
		},

		productCountItems() {
			return Object.entries(this.userAnalytics.products_count).map(([product, count]) => ({
				product,
				count,
			}));
		},
		formattedData() {
			const productCountData = this.userAnalytics.products_count;

			const formattedData = [];

			const userData = {
				"Full Name": this.currentUser.full_name,
				Email: this.currentUser.email,
				"Total Orders": this.userAnalytics.total_orders,
				"Total Spent": this.userAnalytics.total_spent,
				"Most Ordered Product": this.userAnalytics.most_ordered_product,
				"Average Order Value": this.userAnalytics.average_order_value,
				"Total Products Purchased": this.userAnalytics.total_products_purchased,
			};

			formattedData.push(userData);

			for (const [product, count] of Object.entries(productCountData)) {
				// const productCount = { Product: product, Count: count };
				userData[`${product}`] = count;
				// formattedData.push(productCount);
			}
			return formattedData;
		},
		csvFileName() {
			if (this.currentUser) {
				return `user-analytics-${this.currentUser.full_name.replace(/\s+/g, "-")}.csv`;
			}
			return "user-analytics.csv";
		},
	},
	mounted() {
		this.fetchUsers();
	},
};
</script>
