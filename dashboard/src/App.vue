<template>
	<div>
		<router-view />
	</div>
</template>

<script>
export default {
	name: "App",
	inject: ["$auth"],
};
</script>
