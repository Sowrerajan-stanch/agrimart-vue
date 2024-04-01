import { createRouter, createWebHistory } from 'vue-router'

const routes = [
	{
		path: '/Cart',
		name: 'Cart',
		component: () => import('@/pages/Cart.vue'),
	},
	{
		path: '/Products',
		name: 'Products',
		component: () => import('@/pages/Products.vue'),
	},
	{
		path: '/Signup',
		name: 'Signup',
		component: () => import('@/pages/Signup.vue'),
	},
	{
		path: '/Login',
		name: 'Login',
		component: () => import('@/pages/Login.vue'),
	},
	{
		path: '/',
		name: 'Home',
		component: () => import('@/pages/Home.vue'),
	},
]

let router = createRouter({
	history: createWebHistory('/frontend'),
	routes,
})

export default router
