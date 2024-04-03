import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Admin/Dashboard.vue";
import UserReports from "../views/Admin/UserReports.vue";
import authRoutes from "./auth";
import Products from "../views/Products.vue";
import FarmerReports from "../views/Admin/FarmerReports.vue";

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
	{
		path: "/admin",
		name: "Dashboard",
		component: Dashboard,
	},
	{
		path: "/admin/users",
		name: "UserReports",
		component: UserReports,
	},
	{
		path: "/admin/farmers",
		name: "FarmerReports",
		component: FarmerReports,
	},
];

const router = createRouter({
	base: "/dashboard/",
	history: createWebHistory(),
	routes,
});

export default router;
