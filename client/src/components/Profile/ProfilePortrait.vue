// src/components/Profile/ProfilePortrait.vue
<script setup>
import { computed } from 'vue';

const props = defineProps({
  username: {
    type: String,
    default: '用户'
  },
  avatarUrl: {
    type: String,
    required: true 
  },
  gender: {
    type: String,
    default: ''
  }
});


// Vue CLI项目使用 process.env.BASE_URL
// 添加一个简单的检查和回退
const appBaseUrl = (typeof import.meta.env !== 'undefined' && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/';
const defaultAvatar = `${appBaseUrl}images/ProfilePortrait.jpg`; 

const onAvatarError = (event) => {
  console.warn(`Avatar failed to load from: ${event.target.src}. Falling back to default: ${defaultAvatar}`);
  event.target.src = defaultAvatar;
};

// ... (genderIconClass 和 genderColor 计算属性保持不变)
const genderIconClass = computed(() => {
  if (props.gender === 'female' || props.gender === '女') {
    return 'fas fa-venus';
  } else if (props.gender === 'male' || props.gender === '男') {
    return 'fas fa-mars';
  }
  return null;
});

const genderColor = computed(() => {
  if (props.gender === 'female' || props.gender === '女') {
    return 'deeppink';
  } else if (props.gender === 'male' || props.gender === '男') {
    return '#007bff';
  }
  return 'grey';
});
</script>

<template>
  <div class="personal-portrait">
    <div class="avatar-container">
      <img class="avatar" :src="avatarUrl" :alt="username || 'User avatar'" @error="onAvatarError" />
    </div>
    <div class="user-info">
      <span class="username">{{ username || '加载中...' }}</span>
      <span v-if="genderIconClass" class="gender-icon" :style="{ color: genderColor }">
        <i :class="genderIconClass"></i>
      </span>
    </div>
  </div>
</template>

<style scoped>
/* 您的样式保持不变 */
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
  background-color: #f0f0f0;
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