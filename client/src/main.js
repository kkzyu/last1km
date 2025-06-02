import '@fortawesome/fontawesome-free/css/all.css'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'

// 设置axios默认配置
axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.withCredentials = true

// 请求拦截器 - 自动添加认证头
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log('Request headers:', config.headers) // 调试信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理认证错误
axios.interceptors.response.use(
  response => response,
  error => {
    console.error('Response error:', error.response?.data) // 调试信息
    if (error.response && error.response.status === 401) {
      console.log('Token invalid, clearing local storage')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Antd);

// 全局提供 axios
app.config.globalProperties.$axios = axios

app.mount('#app')
