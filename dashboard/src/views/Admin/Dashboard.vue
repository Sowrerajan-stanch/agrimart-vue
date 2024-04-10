<template>
	<AdminNav />
	<p>Users</p>
	<!-- <div class="p-10">
		<div class="flex items-center justify-between px-10">
			<h2 class="text-lg font-semibold text-gray-800">Farmer Analysis</h2>
		</div>
		<div class="flex">
			<div class="flex flex-col gap-5">
				<div v-for="(value, key) in farmerAnalytics" :key="key">
					<div
						v-if="key !== 'products_count'"
						class="w-[300px] bg-white rounded-lg shadow-md overflow-hidden"
					>
						<div class="p-4">
							<h3 class="text-lg font-semibold mb-2">{{ key }}</h3>
							<p class="text-gray-600">{{ value }}</p>
						</div>
					</div>
				</div>
			</div>
			<div class="w-full ml-5 flex flex-col gap-5">
				<div class="flex justify-around">
					<div class="w-[800px] p-5 border rounded">
						<p>Top Selling Products</p>
						<BarChart />
					</div>
					<div class="w-[400px] p-5 border rounded">
						<p>Revenue Distribution by Product Category:</p>
						<div class="flex items-center justify-center">
							<PieChart />
						</div>
					</div>
				</div>
				<div class="flex items-center justify-between">
					<div class="w-[600px] p-5 border rounded">
						<p>Order Status Distribution by Product Category:</p>
						<div class="flex items-center justify-center">
							<DoughtnutChart />
						</div>
					</div>

					<div class="w-[800px] p-5 border rounded">
						<p>Revenue Generated over month</p>
						<LineChart />
					</div>
				</div>
				<div class="h-[500px] mt-5 p-5 border rounded">
					<p>Products Sold out over month</p>
					<Bar :options="chartOptions" :data="chartData" />
				</div>
			</div>
		</div>
	</div> -->
</template>

<script>
import axios from "axios";
import AdminNav from "../../components/Admin/AdminNav.vue";
import LineChart from "../../components/LineChart.vue";
import BarChart from "../../components/BarChart.vue";
import DoughtnutChart from "../../components/DoughtnutChart.vue";
import { Bar } from "vue-chartjs";
import {
	Chart as ChartJS,
	Title,
	Tooltip,
	Legend,
	BarElement,
	LineElement,
	CategoryScale,
	LinearScale,
} from "chart.js";
import PieChart from "../../components/PieChart.vue";
ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale);

export default {
	name: "Dashboard",
	// data() {
	// 	return {
	// 		farmer_analytics: null,
	// 		searchValue: null,
	// 		farmerAnalytics: null,
	// 	};
	// },
	components: {
		AdminNav,
	},
	// mounted() {
	// 	this.fetchFarmerAnalytics();
	// 	this.fetchParticularFarmerAnalytics();
	// },
	// computed: {
	// 	chartData() {
	// 		const months = [
	// 			"January",
	// 			"February",
	// 			"March",
	// 			"April",
	// 			"May",
	// 			"June",
	// 			"July",
	// 			"August",
	// 			"September",
	// 			"October",
	// 			"November",
	// 			"December",
	// 		];
	// 		const counts = Array(12).fill(0);

	// 		if (this.farmer_analytics && this.farmer_analytics.MonthsandCount) {
	// 			for (let i = 0; i < this.farmer_analytics.MonthsandCount.month.length; i++) {
	// 				const month = this.farmer_analytics.MonthsandCount.month[i].split("-")[0];
	// 				const count = this.farmer_analytics.MonthsandCount.count[i];
	// 				const index = months.indexOf(month);
	// 				counts[index] = count;
	// 			}
	// 		}

	// 		return {
	// 			labels: months,
	// 			datasets: [
	// 				{
	// 					label: "Products Sold",
	// 					backgroundColor: "#4CAF50",
	// 					data: counts,
	// 				},
	// 			],
	// 		};
	// 	},
	// 	chartOptions() {
	// 		return {
	// 			responsive: true,
	// 			scales: {
	// 				x: {
	// 					title: {
	// 						display: true,
	// 						text: "Months",
	// 					},
	// 				},
	// 				y: {
	// 					title: {
	// 						display: true,
	// 						text: "Number of Products Sold",
	// 					},
	// 					suggestedMin: 0,
	// 					suggestedMax: 50,
	// 				},
	// 			},
	// 		};
	// 	},
	// 	lineChartData() {
	// 		const data = {
	// 			labels: ["January", "February", "March", "April", "May", "June", "July"],
	// 			datasets: [
	// 				{
	// 					label: "Data One",
	// 					backgroundColor: "#f87979",
	// 					data: [40, 39, 10, 40, 39, 80, 40],
	// 				},
	// 			],
	// 		};

	// 		return data;
	// 	},
	// },
	// methods: {
	// 	async fetchFarmerAnalytics() {
	// 		try {
	// 			const response = await axios.get(
	// 				"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_product_analytics?farmer=FR0001"
	// 			);
	// 			this.farmer_analytics = response.data.message;
	// 			console.log(this.farmer_analytics);
	// 		} catch (error) {
	// 			console.error("Error fetching farmer analytics:", error);
	// 		}
	// 	},
	// 	async fetchParticularFarmerAnalytics(farmerId, farmer) {
	// 		try {
	// 			const response = await axios.get(
	// 				`http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_analytics?farmer=FR0001`
	// 			);
	// 			this.farmerAnalytics = response.data.message;
	// 		} catch (err) {
	// 			console.log(err);
	// 		}
	// 	},
	// },
};
</script>
