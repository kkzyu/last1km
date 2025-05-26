import axios from 'axios';

// 创建axios实例 (与您提供的代码一致)
const api = axios.create({
    baseURL: 'http://localhost:5000/api', // 确保这是正确的API基础URL
    timeout: 15000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// 请求拦截器 (与您提供的代码一致)
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器 (与您提供的代码一致)
api.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        if (error.response) {
            if (error.response.status === 401) {
                localStorage.removeItem('authToken');
                localStorage.removeItem('userInfo');
                if (!window.location.pathname.includes('/login')) {
                    window.location.href = '/login';
                }
                return Promise.reject(new Error('认证失败，请重新登录'));
            }
            const message = error.response.data?.message || '请求失败';
            return Promise.reject(new Error(message));
        }
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
    getOrders: () => api.get('/orders/'), 
    createOrder: (data) => api.post('/orders/', data), 
    getOrderDetails: (id) => api.get(`/orders/${id}`), 
    cancelOrder: (id) => api.post(`/orders/${id}/cancel`), 
    reviewOrder: (id, data) => api.post(`/orders/${id}/review`, data),
    deleteOrder: (id) => api.delete(`/orders/${id}`),
    completeOrder: (id) => api.post(`/orders/${id}/complete`),
    // **新增：图片上传函数**
    uploadOrderImage: (formData) => api.post('/orders/upload_image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data' // 非常重要，用于文件上传
        }
    })
};

export default api;