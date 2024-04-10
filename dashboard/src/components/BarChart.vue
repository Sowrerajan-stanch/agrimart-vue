<template>
	<div class="flex items-center justify-center">
		<canvas ref="barChart" width="500" height="200"></canvas>
	</div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
	mounted() {
		this.fetchFarmerAnalytics();
	},
	methods: {
		renderBarChart() {
			const ctx = this.$refs.barChart.getContext("2d");
			console.log(Object.keys(this.chartData));
			const data = {
				labels: Object.keys(this.chartData),
				datasets: [
					{
						label: "Product Count",
						data: Object.values(this.chartData),
						backgroundColor: "rgba(54, 162, 235, 0.2)",
						borderColor: "rgba(54, 162, 235, 1)",
						borderWidth: 1,
					},
				],
			};
			const options = {
				scales: {
					x: {
						beginAtZero: true,
					},
					y: {
						beginAtZero: true,
					},
				},
			};
			new Chart(ctx, {
				type: "bar",
				data: data,
				options: options,
			});
		},
		async fetchFarmerAnalytics() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_product_analytics?farmer=FR0001"
				);
				this.chartData = response.data.message.product_quantities;
				this.renderBarChart();
			} catch (error) {
				console.error("Error fetching farmer analytics:", error);
			}
		},
	},
	data() {
		return {
			chartData: {},
		};
	},
};
</script>
