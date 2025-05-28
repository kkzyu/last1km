// client/src/plugins/axios.js
import axios from 'axios';
import { message } from 'ant-design-vue';

// 创建axios实例
const instance = axios.create({
  baseURL: '/api',
  timeout: 10000
});

// 请求拦截器 - 添加授权头
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器 - 全局错误处理
instance.interceptors.response.use(
  response => response,
  error => {
    const { response } = error;
    if (response && response.data && response.data.message) {
      message.error(response.data.message);
    } else {
      message.error('请求失败，请稍后重试');
    }
    
    // 处理401错误 - 未授权
    if (response && response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default instance;