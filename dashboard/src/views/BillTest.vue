<template>
	<div>
		<button @click="printBill">Print Bill</button>
		<div id="bill">
			<h1>Bill</h1>
			<table>
				<thead>
					<tr>
						<th>Product</th>
						<th>Price</th>
						<th>Quantity</th>
						<th>Subtotal</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(product, index) in billData.products" :key="index">
						<td>{{ product.name }}</td>
						<td>{{ product.price }}</td>
						<td>{{ product.quantity }}</td>
						<td>{{ product.subtotal }}</td>
					</tr>
				</tbody>
				<tfoot>
					<tr>
						<td colspan="3">Total:</td>
						<td>{{ billData.total }}</td>
					</tr>
				</tfoot>
			</table>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			billData: {
				products: [
					{ name: "Product 1", price: 10, quantity: 2 },
					{ name: "Product 2", price: 15, quantity: 1 },
					{ name: "Product 3", price: 20, quantity: 3 },
					{ name: "Product 4", price: 8, quantity: 4 },
					{ name: "Product 5", price: 12, quantity: 2 },
				],
				total: 0,
			},
		};
	},
	methods: {
		printBill() {
			const prtHtml = document.getElementById("bill").innerHTML;
			const WinPrint = window.open(
				"",
				"",
				"left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0"
			);
			WinPrint.document.write(`<!DOCTYPE html>
        <html>
          <head>
            <title>Bill</title>
            <style>
              table {
                border-collapse: collapse;
                width: 100%;
              }
              th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
              }
              th {
                background-color: #f2f2f2;
              }
            </style>
          </head>
          <body>${prtHtml}</body>
        </html>`);
			WinPrint.document.close();
			WinPrint.focus();
			WinPrint.print();
			WinPrint.close();
		},
	},
};
</script>
