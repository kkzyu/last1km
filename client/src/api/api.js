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
        const token = localStorage.getItem('token');
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
            // 处理 401 错误
            if (error.response.status === 401) {
                // 清除本地存储的认证信息
                localStorage.removeItem('token');
                localStorage.removeItem('userInfo');
                
                // 如果不是登录页面 (基于哈希路由)，则重定向到登录
                if (!window.location.hash.includes('#/login')) {
                    window.location.href = '/#/login'; // 使用哈希路由重定向
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
    updateProfile: (profileData) => api.put('/users/profile', profileData),
    uploadAvatar: (formData) => api.post('/users/upload_avatar', formData, {
        headers: {
            'Content-Type': 'multipart/form-data' // 必须为此类型
        }
    }),
    getAddresses: () => api.get('/users/addresses'),
    addAddress: (addressData) => api.post('/users/addresses', addressData),
    updateAddress: (addressId, addressData) => api.put(`/users/addresses/${addressId}`, addressData),
    deleteAddress: (addressId) => api.delete(`/users/addresses/${addressId}`),
};

export const orderAPI = {
    getOrders: () => api.get('/orders'), 
    createOrder: (data) => api.post('/orders', data), 
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