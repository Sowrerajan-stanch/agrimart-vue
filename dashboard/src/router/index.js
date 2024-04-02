import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from "./auth";
import Products from "../views/Products.vue";

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home,
	},
	...authRoutes,
	{
		path: "/products",
		name: "Products",
		component: Products,
	},
];

const router = createRouter({
	base: "/dashboard/",
	history: createWebHistory(),
	routes,
});

export default router;
