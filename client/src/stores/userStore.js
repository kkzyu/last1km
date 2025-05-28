// src/stores/userStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { userAPI } from '@/api/api'; // 确保您的 api.js 中导出了 userAPI
import { message } from 'ant-design-vue'; // 导入 Ant Design Vue 的 message 组件用于提示

export const useUserStore = defineStore('user', () => {
  // State
  const userProfile = ref(null); // 存储用户资料对象
  const API_BASE_URL = 'http://localhost:5000'; // 用于后端图片及API（如果api.js中没有完全处理）

  // Getters
  const isLoggedIn = computed(() => !!userProfile.value && !!localStorage.getItem('authToken'));
  const displayName = computed(() => {
    if (userProfile.value) {
      return userProfile.value.nickname || userProfile.value.username || '用户';
    }
    return '用户';
  });

  const avatarUrl = computed(() => {
    if (userProfile.value && userProfile.value.avatar) {
      // 处理用户已设置的头像
      if (userProfile.value.avatar.startsWith('http')) {
        return userProfile.value.avatar; // 已经是完整URL
      } else if (userProfile.value.avatar.startsWith('/static/')) {
        // 假设是后端提供的相对路径，相对于API_BASE_URL (例如直接存储 /static/avatars/xxx.png)
         return `${API_BASE_URL}${userProfile.value.avatar}`;
      }
      // 默认假设 avatar 字段是存储在后端 /static/uploads/ 下的文件名
      return `${API_BASE_URL}/static/uploads/${userProfile.value.avatar}`;
    }
    // 处理默认头像，使用应用的基础URL
    const appBaseUrl = (typeof import.meta.env !== 'undefined' && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/';
    return `${appBaseUrl}images/ProfilePortrait.jpg`; // 确保此图片在 public/images/ 目录下
  });

  const gender = computed(() => userProfile.value?.gender);

  // Actions
  async function fetchUserProfile() {
    if (!localStorage.getItem('authToken')) {
      // console.log('No auth token, skipping fetchUserProfile');
      return;
    }
    try {
      const response = await userAPI.getProfile();
      if (response.data && response.data.success) {
        userProfile.value = response.data.data;
      } else {
        console.error('Failed to fetch user profile:', response.data?.message);
        // message.error(response.data?.message || '获取用户资料失败'); // 可选：在这里提示或由调用者处理
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // message.error(error.message || '获取用户资料请求失败'); // 可选
    }
  }

  function setUserProfile(profileData) {
    userProfile.value = profileData;
  }

  function clearUserProfile() {
    userProfile.value = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo'); // 如果您之前有存储这个
    // 在实际应用中，这里可能还需要 router.push('/login');
  }

  // **新增：更新用户资料的 action**
  async function updateUserProfile(profileDataToUpdate) {
    if (!userProfile.value) {
      message.error('用户未登录或资料未加载，无法更新。');
      return false; // 返回false表示操作失败
    }
    try {
      // profileDataToUpdate 应该是一个只包含要更新字段的对象
      // 例如: { nickname: "新的昵称", phone: "138xxxxxx" }
      // 后端 users.py 中的 update_profile 接受 'nickname', 'avatar', 'gender', 'school_info', 'dormitory', 'phone'
      const response = await userAPI.updateProfile(profileDataToUpdate);
      if (response.data && response.data.success) {
        // 后端应该返回更新后的完整用户信息，或者至少是已更新的字段
        // 使用后端返回的数据更新本地store，确保数据一致性
        userProfile.value = { ...userProfile.value, ...response.data.data }; 
        message.success('资料更新成功！');
        return true; // 返回true表示操作成功
      } else {
        message.error(response.data?.message || '更新资料失败');
        return false;
      }
    } catch (error) {
      message.error(error.message || '更新资料请求失败');
      return false;
    }
  }

  return {
    userProfile,
    displayName,
    avatarUrl,
    gender,
    isLoggedIn,
    fetchUserProfile,
    setUserProfile,
    clearUserProfile,
    updateUserProfile, // **确保导出此 action**
    // API_BASE_URL, // 如果其他组件需要直接使用，可以导出，否则内部使用即可
  };
});