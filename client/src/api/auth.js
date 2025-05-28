const API_BASE_URL = 'http://localhost:5000/api/auth';

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

// 注册API
export async function register(userData) {
  return await apiRequest(`${API_BASE_URL}/register`, {
    method: 'POST',
    body: JSON.stringify(userData),
  });
}

// 登录API
export async function login(credentials) {
  return await apiRequest(`${API_BASE_URL}/login`, {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
}

// 登出API
export async function logout() {
  return await apiRequest(`${API_BASE_URL}/logout`, {
    method: 'POST',
  });
}

// 获取用户信息API
export async function getUserProfile() {
  return await apiRequest(`${API_BASE_URL}/profile`);
}

// 更新用户信息API
export async function updateUserProfile(userData) {
  return await apiRequest(`${API_BASE_URL}/profile`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  });
}

// 修改密码API
export async function changePassword(passwordData) {
  return await apiRequest(`${API_BASE_URL}/change-password`, {
    method: 'POST',
    body: JSON.stringify(passwordData),
  });
}

// 验证token API
export async function verifyToken() {
  return await apiRequest(`${API_BASE_URL}/verify-token`, {
    method: 'POST',
  });
}

// 上传头像API
export async function uploadAvatar(formData) {
  const token = localStorage.getItem('authToken');
  const response = await fetch(`${API_BASE_URL}/upload-avatar`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: formData,
  });
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || '上传失败');
  }
  
  return data;
}