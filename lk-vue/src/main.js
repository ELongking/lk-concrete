import {createApp} from "vue"
import App from "./App.vue"
import router from "./router"
import ElementPlus from 'element-plus'
import axios from "axios"
import "element-plus/theme-chalk/index.css"

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(router).use(ElementPlus).mount("#app")