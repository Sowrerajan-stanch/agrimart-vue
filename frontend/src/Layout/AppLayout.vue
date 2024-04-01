<template>
	<Navbar></Navbar>
	<slot />
</template>
<script>
import Navbar from '../components/Navbar.vue'
export default {
	name: 'AppLayout',
	components: {
		Navbar,
	},
}
</script>
