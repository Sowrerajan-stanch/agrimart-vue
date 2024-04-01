<template>
	<div>
		<router-view />
	</div>
</template>
<script setup>
import { createDocumentResource, createListResource } from 'frappe-ui'
import { toRaw } from 'vue'

let user_doc = toRaw(
	createListResource({
		doctype: 'AgriUser',
		fields: ['full_name', 'address', 'email'],
	})
)
console.log(user_doc)
</script>
