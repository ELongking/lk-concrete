import {createApp} from "vue"
import App from "./App.vue"
import router from "./router"
import ElementPlus from 'element-plus'
import axios from "axios"

import "element-plus/theme-chalk/index.css"
import * as ElementPlusIconsVue from "@element-plus/icons-vue"

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(router).use(ElementPlus).mount("#app")
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}