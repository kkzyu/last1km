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
    <div class="user-info-container">
      <span class="username">{{ username || '加载中...' }}</span>
      <span v-if="genderIconClass" class="gender-icon" :style="{ color: genderColor }">
        <i :class="genderIconClass"></i>
      </span>
    </div>
  </div>
</template>

<style scoped>
/* 美化后的个人肖像样式 - 垂直布局，放大头像 */
.personal-portrait {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 水平居中 */
  gap: 16px; /* 头像和信息之间的间距 */
  padding: 30px 20px 20px; /* 顶部留多点空间，整体内边距 */
  margin: 0; /* 移除外部的 margin，让父组件控制 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif; /* 圆润的无衬线字体 */
}

.avatar-container {
  flex-shrink: 0;
  position: relative; /* 为可能的徽章等元素准备 */
}

.avatar {
  object-fit: cover;
  border-radius: 50%;
  width: 100px; /* 放大头像 */
  height: 100px; /* 放大头像 */
  border: 3px solid #fff; /* 白色边框 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); /* 更柔和的阴影 */
  background-color: #f8f9fa; /* 占位背景色 */
  transition: transform 0.2s ease-in-out;
}

.avatar:hover {
  transform: scale(1.02); /* 轻微放大效果 */
}

/* Changed from .user-info to .user-info-container to reflect template change and new layout */
.user-info-container { 
  display: flex;
  flex-direction: row; /* Username and gender icon in a row */
  align-items: baseline; /* Align items by their baseline */
  justify-content: center; /* Center the row content */
  gap: 8px; /* Space between username and gender icon */
  text-align: center;
  margin-top: 12px; /* Add some space below the avatar */
}

.username {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif; /* 更圆润的字体 */
  font-size: 1.4rem; /* 放大用户名 */
  font-weight: 600; /* 略粗的字体 */
  color: #2c3e50; /* 深蓝灰色 */
  letter-spacing: 0.3px;
  line-height: 1.2;
}

.gender-icon {
  font-size: 1.1rem; /* 放大性别图标 */
  opacity: 0.8;
  transition: opacity 0.2s ease-in-out;
}

.gender-icon:hover {
  opacity: 1;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .personal-portrait {
    padding: 25px 15px 15px;
    gap: 14px;
  }
  
  .avatar {
    width: 85px; /* 移动端略小一点 */
    height: 85px;
    border-width: 2px;
  }
  
  .username {
    font-size: 1.2rem;
  }
  
  .gender-icon {
    font-size: 1rem;
  }
}
</style>