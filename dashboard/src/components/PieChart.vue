<template>
	<div>
		<canvas ref="pieChart" width="400" height="400"></canvas>
	</div>
</template>

<script>
import Chart from "chart.js/auto";
import axios from "axios";

export default {
	mounted() {
		this.fetchRevenueDistribution();
	},
	methods: {
		async fetchRevenueDistribution() {
			try {
				const response = await axios.get(
					"http://agri-app.localhost:8080/api/method/agriapp.farmer.farmer_product_analytics?farmer=FR0001"
				);
				this.renderPieChart(response.data.message.revenue_distribution);
			} catch (error) {
				console.error("Error fetching revenue distribution:", error);
			}
		},
		renderPieChart(revenueDistribution) {
			const ctx = this.$refs.pieChart.getContext("2d");
			const data = {
				labels: Object.keys(revenueDistribution),
				datasets: [
					{
						label: "Revenue",
						data: Object.values(revenueDistribution),
						backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
						borderWidth: 1,
					},
				],
			};
			new Chart(ctx, {
				type: "pie",
				data: data,
			});
		},
	},
};
</script>
