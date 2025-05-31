import '@fortawesome/fontawesome-free/css/all.css'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import api from './api/api' // 导入axios实例

// 设置axios默认Authorization头，如果localStorage中有token
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd);

app.mount('#app')
