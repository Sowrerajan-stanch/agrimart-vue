<template>
	<Dialog v-model:visible="visible" header="User Analytics" @hide="hideDialog">
		<div class="p-5">
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
				<div
					v-for="(value, key) in analytics"
					:key="key"
					class="bg-white rounded-lg shadow-md overflow-hidden"
				>
					<div class="p-4">
						<h3 class="text-lg font-semibold mb-2">{{ key }}</h3>
						<p class="text-gray-600">{{ value }}</p>
					</div>
				</div>
			</div>
		</div>
	</Dialog>
</template>

<script>
import Dialog from "primevue/dialog";

export default {
	name: "UserAnlyticsDialog",
	components: {
		Dialog,
	},
	props: {
		visible: Boolean,
		analytics: Object,
	},
	setup(props) {
		console.log(props);
		const visible = props.visible;
		console.log("vichible", visible);
		const hideDialog = () => {
			visible = false;
		};

		return {
			visible,
			hideDialog,
		};
	},
};
</script>
