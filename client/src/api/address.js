const API_BASE_URL = 'http://localhost:5000/api/address';

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
  const token = localStorage.getItem('authToken');
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

// 获取地址列表
export async function getAddresses(type = null) {
  const url = type ? `${API_BASE_URL}/list?type=${type}` : `${API_BASE_URL}/list`;
  return await apiRequest(url);
}

// 添加地址
export async function addAddress(addressData) {
  return await apiRequest(`${API_BASE_URL}/add`, {
    method: 'POST',
    body: JSON.stringify(addressData),
  });
}

// 更新地址
export async function updateAddress(addressId, addressData) {
  return await apiRequest(`${API_BASE_URL}/update/${addressId}`, {
    method: 'PUT',
    body: JSON.stringify(addressData),
  });
}

// 删除地址
export async function deleteAddress(addressId) {
  return await apiRequest(`${API_BASE_URL}/delete/${addressId}`, {
    method: 'DELETE',
  });
}

// 获取默认地址
export async function getDefaultAddresses() {
  return await apiRequest(`${API_BASE_URL}/default`);
}

// 设置默认地址
export async function setDefaultAddress(addressId) {
  return await apiRequest(`${API_BASE_URL}/set-default/${addressId}`, {
    method: 'POST',
  });
}