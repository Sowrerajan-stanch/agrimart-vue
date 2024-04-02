export default [
	{
		path: "/login",
		name: "Login",
		component: () => import(/* webpackChunkName: "login" */ "../views/Login.vue"),
		meta: {
			isLoginPage: true,
		},
		props: true,
	},
	{
		path: "/cart",
		name: "Cart",
		component: () => import(/* webpackChunkName: "cart" */ "../views/Cart.vue"),
		// meta: {
		// 	isLoginPage: true,
		// },
		props: true,
	},
	{
		path: "/orders",
		name: "Orders",
		component: () => import(/* webpackChunkName: "orders" */ "../views/Orders.vue"),
		// meta: {
		// 	isLoginPage: true,
		// },
		props: true,
	},
];
