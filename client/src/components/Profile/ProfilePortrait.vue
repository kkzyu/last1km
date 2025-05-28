<template>
  <div class="personal-portrait">
    <div class="avatar-container">
      <img 
        class="avatar" 
        :src="userInfo.avatar || './images/ProfilePortrait.jpg'" 
        :alt="`${userInfo.nickname || userInfo.username}的头像`" 
        @error="handleImageError"
      />
    </div>
    <div class="user-info">
      <span class="username">{{ userInfo.nickname || userInfo.username || '未知用户' }}</span>
      <span class="gender-icon" v-if="userInfo.gender">
        <i :class="getGenderIcon(userInfo.gender)"></i>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getUserProfile } from '@/api/auth.js';

const userInfo = ref({
  id: null,
  username: '',
  nickname: '',
  avatar: '',
  gender: '',
  phone: '',
  email: '',
  dormitory: ''
});

onMounted(async () => {
  await loadUserInfo();
});

const loadUserInfo = async () => {
  try {
    // 先从localStorage获取缓存的用户信息
    const cachedUserInfo = localStorage.getItem('userInfo');
    if (cachedUserInfo) {
      userInfo.value = { ...userInfo.value, ...JSON.parse(cachedUserInfo) };
    }
    
    // 然后从API获取最新的用户信息
    const response = await getUserProfile();
    if (response.code === 200) {
      userInfo.value = { ...userInfo.value, ...response.data.user };
      // 更新localStorage缓存
      localStorage.setItem('userInfo', JSON.stringify(response.data.user));
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
    // 如果API调用失败，保持使用localStorage中的缓存信息
  }
};

const getGenderIcon = (gender) => {
  const genderIcons = {
    'male': 'fas fa-mars',
    'female': 'fas fa-venus',
    '男': 'fas fa-mars',
    '女': 'fas fa-venus'
  };
  return genderIcons[gender] || 'fas fa-question';
};

const handleImageError = (event) => {
  // 头像加载失败时使用默认头像
  event.target.src = './images/ProfilePortrait.jpg';
};

// 暴露方法供父组件调用
defineExpose({
  loadUserInfo
});
</script>

<style scoped>
.personal-portrait {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  margin: 20px 0 0 5px;
}

.avatar-container {
  flex-shrink: 0;
}

.avatar {
  object-fit: cover;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

.gender-icon {
  font-size: 0.9rem;
}

.gender-icon .fa-mars {
  color: #4a90e2;
}

.gender-icon .fa-venus {
  color: deeppink;
}

.gender-icon .fa-question {
  color: #999;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .avatar {
    width: 50px;
    height: 50px;
  }
  
  .username {
    font-size: 1rem;
  }
}
</style>