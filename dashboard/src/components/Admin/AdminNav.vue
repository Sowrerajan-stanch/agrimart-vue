<template>
	<Menubar :model="items" class="p-menubar border">
		<template #start>
			<svg
				width="35"
				height="40"
				viewBox="0 0 35 40"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
				class="h-8"
			>
				<path d="..." class="fill-primary-500 dark:fill-primary-400" />
				<path d="..." class="fill-surface-700 dark:fill-surface-0/80" />
			</svg>
		</template>
		<template #item="{ item, props, hasSubmenu, root }">
			<a v-ripple class="flex items-center" v-bind="props.action">
				<router-link v-if="item.url" :to="item.url" class="flex items-center">
					<span :class="item.icon" />
					<span class="ml-2">{{ item.label }}</span>
					<Badge
						v-if="item.badge"
						:class="{ 'ml-auto': !root, 'ml-2': root }"
						:value="item.badge"
					/>
				</router-link>
				<span
					v-if="item.shortcut"
					class="ml-auto border border-surface-200 dark:border-surface-500 rounded-md bg-surface-100 dark:bg-surface-800 text-xs p-1"
					>{{ item.shortcut }}</span
				>
				<i
					v-if="hasSubmenu"
					:class="[
						'pi pi-angle-down text-primary-500 dark:text-primary-400-500 dark:text-primary-400',
						{ 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root },
					]"
				></i>
			</a>
		</template>
		<template #end>
			<div class="flex items-center gap-2">
				<Avatar
					image="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg"
					shape="circle"
				/>
				<Button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</Button>
			</div>
		</template>
	</Menubar>
</template>
<script>
import Menubar from "primevue/menubar";
import InputText from "primevue/inputtext";
import Badge from "primevue/badge";
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import { RouterLink } from "vue-router";
import axios from "axios";

export default {
	name: "Navbar",
	data() {
		return {
			items: [
				{
					label: "Home",
					icon: "pi pi-home",
					url: "/admin/",
				},
				{
					label: "Users",
					icon: "pi pi-user",
					url: "/admin/users",
				},
				{
					label: "Farmers",
					icon: "pi-pi-prime",
					url: "/admin/farmers",
				},
			],
		};
	},

	inject: ["$auth"],
	components: {
		Menubar,
		InputText,
		Badge,
		Avatar,
		Button,
		RouterLink,
	},
};
</script>
