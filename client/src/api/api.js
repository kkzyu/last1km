import axios from 'axios';

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
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        // 调试信息
        console.log('API Request:', {
            method: config.method,
            url: config.url,
            baseURL: config.baseURL,
            fullURL: `${config.baseURL}${config.url}`,
            headers: config.headers
        });
        
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器
api.interceptors.response.use(
    response => {
        console.log('API Response:', {
            status: response.status,
            url: response.config.url
        });
        return response;
    },
    async error => {
        console.error('API Error Details:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            url: error.config?.url,
            method: error.config?.method,
            headers: error.config?.headers,
            data: error.response?.data
        });
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
    
    // 聊天相关API
    sendChatMessage: (messageData) => api.post('/chat', messageData),
    getChatHistory: () => api.get('/chat/history'),
    clearChatHistory: () => api.delete('/chat/clear'),
};

export const orderAPI = {
    getOrders: () => api.get('/orders'), 
    createOrder: (data) => api.post('/orders', data), 
    getOrderDetails: (id) => api.get(`/orders/${id}`), 
    cancelOrder: (id) => api.post(`/orders/${id}/cancel`), 
    reviewOrder: (id, data) => api.post(`/orders/${id}/review`, data),
    deleteOrder: (id) => api.delete(`/orders/${id}`),
    completeOrder: (id) => api.post(`/orders/${id}/complete`),
    
    analyzeOrderImage: (data) => api.post('/orders/analyze-image', data),
    uploadOrderImage: (formData) => api.post('/orders/upload_image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
};

export const mapAPI = {
    getMapConfig: () => api.get('/map/config'),
    searchPlaces: (keyword, city = '杭州') => 
        api.post('/map/search', { keyword, city }),
    calculateRoute: (routeData) => 
        api.post('/map/route', routeData),
};

export default api;