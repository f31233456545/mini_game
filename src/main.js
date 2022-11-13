import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import createPopup from './utils/popup.js'


const app = createApp(App)
    .use(router)
    .use(store)
    .use(ElementPlus)

app.config.globalProperties.$popup = createPopup

app.mount('#app')
