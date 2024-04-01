import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import App from './App.vue'

import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

let app = createApp(App)
let pinia = createPinia()

setConfig('resourceFetcher', frappeRequest)

app.use(router)
app.use(pinia)
pinia.use(piniaPluginPersistedstate)
app.use(resourcesPlugin)

app.component('Button', Button)
app.mount('#app')
