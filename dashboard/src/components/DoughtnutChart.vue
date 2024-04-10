<template>
	<div>
		<canvas ref="donutChart" width="400" height="400"></canvas>
	</div>
</template>

<script>
import Chart from "chart.js/auto";
import axios from "axios";

export default {
	mounted() {
		this.fetchOrderStatusDistribution();
	},
	methods: {
		async fetchOrderStatusDistribution() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_product_analytics?farmer=FR0001"
				);
				this.renderDonutChart(response.data.message.status_distribution);
			} catch (error) {
				console.error("Error fetching order status distribution:", error);
			}
		},
		renderDonutChart(statusDistribution) {
			const ctx = this.$refs.donutChart.getContext("2d");
			const data = {
				labels: Object.keys(statusDistribution),
				datasets: [
					{
						label: "Order Status",
						data: Object.values(statusDistribution),
						backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"], // Example colors
						borderWidth: 1,
					},
				],
			};
			new Chart(ctx, {
				type: "doughnut",
				data: data,
			});
		},
	},
};
</script>
