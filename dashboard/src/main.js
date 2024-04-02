import { createApp, reactive } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";

import router from "./router";
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";
import ToastService from "primevue/toastservice";

// Css
import "primevue/resources/themes/aura-light-green/theme.css";
import "./style.css";

const app = createApp(App);
const auth = reactive(new Auth());

// Plugins
app.use(router);
app.use(resourceManager);
app.use(PrimeVue);
app.use(ToastService);

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);

// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		console.log(auth.isLoggedIn);
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: "Login", query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: "Home" });
		} else {
			next();
		}
	}
});

app.mount("#app");
