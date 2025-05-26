import axios from 'axios';
import { useRouter } from 'vue-router';

// 创建axios实例
const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    timeout: 15000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// 请求拦截器
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        
        // 删除预检请求的重定向配置
        delete config.redirect;
        
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器
api.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        if (error.response) {
            // 处理 401 错误
            if (error.response.status === 401) {
                // 清除本地存储的认证信息
                localStorage.removeItem('authToken');
                localStorage.removeItem('userInfo');
                
                // 如果不是登录页面，则重定向到登录
                if (!window.location.pathname.includes('/login')) {
                    window.location.href = '/login';
                }
                return Promise.reject(new Error('认证失败，请重新登录'));
            }
            
            // 处理其他HTTP错误
            const message = error.response.data?.message || '请求失败';
            return Promise.reject(new Error(message));
        }
        
        // 处理网络错误
        if (error.code === 'ERR_NETWORK') {
            return Promise.reject(new Error('网络连接失败，请检查网络'));
        }
        
        return Promise.reject(error);
    }
);

export const authAPI = {
    login: (credentials) => api.post('/auth/login', credentials),
    register: (userData) => api.post('/auth/register', userData),
};

export const userAPI = {
    getProfile: () => api.get('/users/profile'),
    updateProfile: (data) => api.put('/users/profile', data),
    getAddresses: () => api.get('/users/addresses'),
    addAddress: (data) => api.post('/users/addresses', data),
    updateAddress: (id, data) => api.put(`/users/addresses/${id}`, data),
    deleteAddress: (id) => api.delete(`/users/addresses/${id}`),
};

export const orderAPI = {
    getOrders: () => api.get('/orders'),
    createOrder: (data) => api.post('/orders', data),
    getOrderDetails: (id) => api.get(`/orders/${id}`),
    cancelOrder: (id) => api.post(`/orders/${id}/cancel`),
};

export default api;
