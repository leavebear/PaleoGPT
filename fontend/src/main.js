import './assets/main.scss'

import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from '@/router'
import { createPinia } from 'pinia'
import { createPersistedState} from 'pinia-persistedstate-plugin'
import App from './App.vue'
import locale from 'element-plus/dist/locale/zh-cn.js'

const pinia = createPinia()
const persist = createPersistedState()
const app = createApp(App);
app.use(router);
app.use(pinia);
pinia.use(persist)
app.mount("#app")
app.use(ElementPlus,{locale})