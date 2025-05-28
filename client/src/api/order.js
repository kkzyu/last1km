const API_BASE_URL = 'http://localhost:5000/api/orders';

// API请求封装
async function apiRequest(url, options = {}) {
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // 如果需要认证，添加token
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('API请求失败:', error);
    throw error;
  }
}

// 创建订单
export async function createOrder(orderData) {
  return await apiRequest(`${API_BASE_URL}/create`, {
    method: 'POST',
    body: JSON.stringify(orderData),
  });
}

// 上传订单图片
export async function uploadOrderImage(formData) {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/upload-image`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: formData, // FormData对象，不设置Content-Type
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || '上传失败');
  }
  
  return data;
}

// 获取我的订单列表
export async function getMyOrders(params = {}) {
  const queryParams = new URLSearchParams(params);
  return await apiRequest(`${API_BASE_URL}/my-orders?${queryParams}`);
}

// 获取订单详情
export async function getOrderDetail(orderId) {
  return await apiRequest(`${API_BASE_URL}/${orderId}`);
}

// 取消订单
export async function cancelOrder(orderId) {
  return await apiRequest(`${API_BASE_URL}/${orderId}/cancel`, {
    method: 'PUT',
  });
}

// 恢复订单
export async function restoreOrder(orderId) {
  return await apiRequest(`${API_BASE_URL}/${orderId}/restore`, {
    method: 'PUT',
  });
}

// 评价订单
export async function reviewOrder(orderId, reviewData) {
  return await apiRequest(`${API_BASE_URL}/${orderId}/review`, {
    method: 'POST',
    body: JSON.stringify(reviewData),
  });
}

// 获取订单统计
export async function getOrderStatistics() {
  return await apiRequest(`${API_BASE_URL}/statistics`);
}