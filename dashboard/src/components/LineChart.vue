<template>
	<Line :options="lineChartOptions" :data="lineChartData" />
</template>

<script>
import axios from "axios";
import { Line } from "vue-chartjs";
import {
	Chart as ChartJS,
	Title,
	Tooltip,
	Legend,
	LineElement,
	CategoryScale,
	PointElement,
	LinearScale,
} from "chart.js";
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
	name: "Dashboard",
	data() {
		return {
			farmer_analytics: null,
			searchValue: null,
		};
	},
	components: {
		Line,
	},
	mounted() {
		this.fetchFarmerAnalytics();
	},
	computed: {
		lineChartData() {
			const revenueData = this.farmer_analytics?.revenueGenerated || {};
			const months = revenueData.month || [];
			const revenue = revenueData.revenue || [];

			return {
				labels: months,
				datasets: [
					{
						label: "Revenue Generated",
						backgroundColor: "rgba(75, 192, 192, 0.2)",
						borderColor: "rgba(75, 192, 192, 1)",
						borderWidth: 1,
						data: revenue,
					},
				],
			};
		},
		lineChartOptions() {
			return {
				responsive: true,
				scales: {
					x: {
						title: {
							display: true,
							text: "Month",
						},
					},
					y: {
						title: {
							display: true,
							text: "Revenue Generated",
						},
						beginAtZero: true,
					},
				},
			};
		},
	},
	methods: {
		async fetchFarmerAnalytics() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_product_analytics?farmer=FR0001"
				);
				this.farmer_analytics = response.data.message;
			} catch (error) {
				console.error("Error fetching farmer analytics:", error);
			}
		},
	},
};
</script>
