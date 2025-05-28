import '@fortawesome/fontawesome-free/css/all.css'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'


const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Antd);

const userStore = useUserStore()
userStore.initFromStorage()

app.mount('#app')
