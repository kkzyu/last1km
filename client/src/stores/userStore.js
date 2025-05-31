// src/stores/userStore.js
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import api, { userAPI } from '@/api/api';
import { message } from 'ant-design-vue';

const API_BASE_URL = 'http://localhost:5000';
const MAX_RECENT_ACCOUNTS = 5; // 最多保存最近5个账号

export const useUserStore = defineStore('user', () => {
  const userProfile = ref(null);
  const isLoadingProfile = ref(false);
  const token = ref(localStorage.getItem('token') || null);
  const recentAccounts = ref(JSON.parse(localStorage.getItem('recentAccounts') || '[]'));

  const isLoggedIn = computed(() => !!token.value && !!userProfile.value);

  const displayName = computed(() => {
    if (userProfile.value) {
      return userProfile.value.nickname || userProfile.value.username || '用户';
    }
    return '用户';
  });

  const avatarUrl = computed(() => {
    if (userProfile.value && userProfile.value.avatar) {
      if (userProfile.value.avatar.startsWith('http')) {
        return userProfile.value.avatar;
      } else if (userProfile.value.avatar.startsWith('/static/')) {
         return `${API_BASE_URL}${userProfile.value.avatar}`;
      }
      return `${API_BASE_URL}/static/uploads/${userProfile.value.avatar}`;
    }
    const appBaseUrl = (typeof import.meta.env !== 'undefined' && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/';
    return `${appBaseUrl}images/ProfilePortrait.jpg`;
  });

  const gender = computed(() => userProfile.value?.gender);


  function updateRecentAccounts(profile) {
    if (!profile || !profile.username) return;

    const existingAccountIndex = recentAccounts.value.findIndex(acc => acc.username === profile.username);
    if (existingAccountIndex > -1) {
      // 如果已存在，移到最前面
      recentAccounts.value.splice(existingAccountIndex, 1);
    }

    // 修复头像 URL 处理逻辑
    let profileAvatarUrl;
    if (profile.avatar) {
      if (profile.avatar.startsWith('http://') || profile.avatar.startsWith('https://')) {
        // 完整的 HTTP/HTTPS URL
        profileAvatarUrl = profile.avatar;
      } else if (profile.avatar.startsWith('/static/')) {
        // 服务器静态路径
        profileAvatarUrl = `${API_BASE_URL}${profile.avatar}`;
      } else if (profile.avatar.startsWith('/')) {
        // 其他绝对路径
        profileAvatarUrl = `${API_BASE_URL}${profile.avatar}`;
      } else {
        // 相对路径，假设是上传的文件名
        profileAvatarUrl = `${API_BASE_URL}/static/uploads/${profile.avatar}`;
      }
    } else {
      // 没有头像时使用默认标识
      profileAvatarUrl = 'DEFAULT_AVATAR';
    }

    recentAccounts.value.unshift({
      username: profile.username,
      displayName: profile.nickname || profile.username,
      avatarUrl: profileAvatarUrl
    });

    // 限制最近账户数量
    if (recentAccounts.value.length > 5) {
      recentAccounts.value = recentAccounts.value.slice(0, 5);
    }

    // 保存到本地存储
    localStorage.setItem('recentAccounts', JSON.stringify(recentAccounts.value));
  }

  function removeRecentAccount(username) {
    recentAccounts.value = recentAccounts.value.filter(acc => acc.username !== username);
    localStorage.setItem('recentAccounts', JSON.stringify(recentAccounts.value));
  }


  async function fetchUserProfile() {
    const currentToken = localStorage.getItem('token'); // Use currentToken to avoid closure issues with ref
    if (!currentToken) {
      userProfile.value = null;
      return;
    }
    // Ensure Authorization header is set for this request
    // This should ideally be handled by an Axios interceptor that reads token.value
    // For now, let's assume the interceptor is correctly set up or set it explicitly if needed.
    // api.defaults.headers.common['Authorization'] = `Bearer ${currentToken}`;


    isLoadingProfile.value = true;
    try {
      const response = await userAPI.getProfile();
      if (response.data && response.data.success) {
        userProfile.value = response.data.data;
        // token.value = currentToken; // Ensure token ref is also in sync if needed, though it's read from localStorage.getItem('token')
                                   // This line might be redundant if token.value is already set from localStorage.getItem('token')
        updateRecentAccounts(userProfile.value); // 更新最近账户列表
      } else {
        userProfile.value = null;
        // If fetching profile fails (e.g. token expired), clear the token
        // localStorage.removeItem('token');
        // token.value = null;
        // message.error(response.data?.message || '获取用户资料失败，请重新登录');
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      userProfile.value = null;
      // Also clear token on network error or other exceptions during profile fetch
      // localStorage.removeItem('token');
      // token.value = null;
      // message.error('获取用户资料时发生错误，请检查网络连接或稍后重试。');
    } finally {
      isLoadingProfile.value = false;
    }
  }

  function loginSuccess(_token, profile) {
    token.value = _token;
    localStorage.setItem('token', _token);
    userProfile.value = profile;
    api.defaults.headers.common['Authorization'] = `Bearer ${_token}`;
    updateRecentAccounts(profile); // 登录成功后更新最近账户
  }
  function clearUserProfile() {
    userProfile.value = null;
    token.value = null;
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  }

  function setUserProfile(profile) {
    userProfile.value = profile;
    if (profile) {
        updateRecentAccounts(profile);
    }
  }

  async function updateUserProfile(dataToUpdate) {
    if (!userProfile.value) {
        message.error('用户未登录');
        return false;
    }
    isLoadingProfile.value = true;
    try {
        const response = await userAPI.updateProfile(dataToUpdate);
        if (response.data && response.data.success) {
            userProfile.value = { ...userProfile.value, ...response.data.data };
            updateRecentAccounts(userProfile.value); // 更新信息后也更新最近账户列表
            message.success('资料更新成功！');
            return true;
        } else {
            message.error(response.data?.message || '资料更新失败');
            return false;
        }
    } catch (error) {
        message.error(error.response?.data?.message || error.message || '更新请求失败');
        return false;
    } finally {
        isLoadingProfile.value = false;
    }
  }

  async function uploadUserAvatar(avatarFile) {
    if (!userProfile.value) {
      message.error('用户未登录，无法上传头像。');
      return false;
    }
    isLoadingProfile.value = true;
    try {
      const formData = new FormData();
      formData.append('avatar', avatarFile);

      const response = await userAPI.uploadAvatar(formData);

      if (response.data && response.data.success) {
        // Assuming the response.data.data contains the updated user object or at least the new avatar URL
        // If it's the full user object:
        userProfile.value = response.data.data.user; // or response.data.data if that's the user object
        // If it's just the avatar URL string:
        // userProfile.value.avatar = response.data.data.avatarUrl;
        updateRecentAccounts(userProfile.value); // 更新头像后也更新最近账户列表
        message.success('头像上传成功！');
        return true;
      } else {
        message.error(response.data?.message || '头像上传失败');
        return false;
      }
    } catch (error) {
      message.error(error.response?.data?.message || error.message || '头像上传请求失败');
      return false;
    } finally {
      isLoadingProfile.value = false;
    }
  }


  return {
    userProfile,
    isLoadingProfile,
    token,
    isLoggedIn,
    displayName,
    avatarUrl,
    gender,
    recentAccounts, // 导出最近账户列表
    fetchUserProfile,
    loginSuccess,
    setUserProfile,
    clearUserProfile,
    updateUserProfile,
    uploadUserAvatar,
    removeRecentAccount, // 导出移除函数
  };
});