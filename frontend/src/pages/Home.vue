<template>
	<Navbar />
	<div>Hello</div>
</template>

<script>
import { Dialog } from 'frappe-ui'
import Navbar from '../components/Navbar.vue'

export default {
	name: 'Home',
	data() {
		return {
			showDialog: false,
		}
	},
	resources: {
		ping: {
			url: 'ping',
		},
	},
	components: {
		Dialog,
		Navbar,
	},
}
</script>
