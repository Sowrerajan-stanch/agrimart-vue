import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Admin/Dashboard.vue";
import UserReports from "../views/Admin/UserReports.vue";
import authRoutes from "./auth";
import Products from "../views/Products.vue";
import FarmerReports from "../views/Admin/FarmerReports.vue";
import VendorDashboard from "../views/Vendor/Dashboard.vue";
import VendorProducts from "../views/Vendor/Products.vue";
import Buyers from "../views/Vendor/Buyers.vue";
import BillTest from "../views/BillTest.vue";

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
		meta: { requiresAdmin: true },
	},
	{
		path: "/admin/users",
		name: "UserReports",
		component: UserReports,
		meta: { requiresAdmin: true },
	},
	{
		path: "/admin/farmers",
		name: "FarmerReports",
		component: FarmerReports,
		meta: { requiresAdmin: true },
	},
	{
		path: "/vendor/",
		name: "VendorDashboard",
		component: VendorDashboard,
		meta: { requiresVendor: true },
	},
	{
		path: "/vendor/products",
		name: "VendorProducts",
		component: VendorProducts,
		meta: { requiresVendor: true },
	},
	{
		path: "/vendor/buyers",
		name: "Buyers",
		component: Buyers,
		meta: { requiresVendor: true },
	},
	{
		path: "/billtest",
		name: "Billtest",
		component: BillTest,
	},
];

const router = createRouter({
	base: "/dashboard/",
	history: createWebHistory(),
	routes,
});

router.beforeEach((to, from, next) => {
	const isAuthenticated = () => {
		const token = localStorage.getItem("token") || sessionStorage.getItem("token");
		return !!token;
	};

	const isAdmin = () => {
		const userRole = localStorage.getItem("role") || sessionStorage.getItem("role");
		return userRole === "admin";
	};

	const isVendor = () => {
		const userRole = localStorage.getItem("role") || sessionStorage.getItem("role");
		return userRole === "vendor";
	};

	if (to.meta.requiresAdmin && !isAdmin) {
		next({ name: "Home" });
	} else if (to.meta.requiresVendor && !isVendor) {
		next({ name: "Home" });
	} else {
		next();
	}
});

export default router;
