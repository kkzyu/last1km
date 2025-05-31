<template>
  <div class="page-container">
    <ProfilePortrait 
      :username="userStore.displayName"
      :avatarUrl="userStore.avatarUrl"
      :gender="userStore.gender"
    />
    <div class="profile-actions-container"> <!-- New container for actions -->
      <div class="profile-info-group"> <!-- Group for personal info and orders -->
        <div class="personal-info" @click="navigateTo('/profile/personal')"> <!-- Moved click handler here -->
          <span class="icon1"><i class="fas fa-address-card"></i></span>
          <p class="description">个人资料</p>
          <span class="icon2"><i class="fas fa-angle-right"></i></span> <!-- Removed click handler from icon -->
        </div>
        <div class="personal-info" @click="navigateTo('/profile/orders')"> <!-- Moved click handler here -->
          <span class="icon1"><i class="fas fa-bars"></i></span>
          <p class="description">历史订单</p>
          <span class="icon2"><i class="fas fa-angle-right"></i></span> <!-- Removed click handler from icon -->
        </div>
      </div>

      <div class="profile-info-group"> <!-- Separate group for contact -->
        <div class="personal-info"> <!-- This item does not navigate, so no top-level click handler -->
          <span class="icon1"><i class="fas fa-headphones"></i></span>
          <p class="description">联系客服</p>
          <span class="icon2"><i class="fas fa-angle-right"></i></span> 
        </div>
      </div>
    </div>

    <!-- Slogan container removed -->

    <!-- Removed account actions -->
  </div>
  <BottomNav />
</template>

<script setup>
import { onMounted } from 'vue';
import ProfilePortrait from '@/components/Profile/ProfilePortrait.vue';
import BottomNav from '@/components/Bottom/BottomNav.vue';
import { useUserStore } from '@/stores/userStore'; // 导入 user store
import { useRouter } from 'vue-router'; // 导入 useRouter
// import { message } from 'ant-design-vue'; // message不再在此组件中使用

// const $route = useRoute() // 如果不再直接使用 $route 可以移除，或者从 vue-router 导入 useRoute
const router = useRouter(); // 获取 router 实例
const userStore = useUserStore(); // 获取 user store 实例

onMounted(() => {
  // 如果 store 中没有用户数据，则尝试从后端获取
  // 这假设用户直接访问此页面时可能没有预先加载数据
  if (!userStore.userProfile) {
    userStore.fetchUserProfile();
  }
});

const navigateTo = (path) => {
  router.push(path);
};

// Removed switchToAccount and logout methods

</script>

<style scoped>
/* 您的样式保持不变，只确保 FontAwesome 图标库已正确引入 */
@import url("https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/font-awesome/4.7.0/css/font-awesome.min.css");
/* 如果您使用的是 FontAwesome 5+，导入方式可能不同，例如通过 main.js 全局导入或使用专用 Vue 组件 */
/* @import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"); */

.page-container {
  display: flex; /* New */
  flex-direction: column; /* New */
  background-color: #f8f9fa; /* 淡灰色背景 */
  padding: 20px;
  padding-bottom: 20px; /* Adjusted from 100px */
  min-height: 100vh; /* 确保页面至少撑满整个视窗高度 */
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif; /* 圆润的无衬线字体 */
}

.profile-actions-container {
  margin-top: 28px; /* 略微增加与上方头像区域的间距 */
  display: flex;
  flex-direction: column;
  gap: 20px; /* 增加卡片组之间的间距 */
}

.profile-info-group {
  background-color: #ffffff; /* 白色卡片 */
  border-radius: 15px; 
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.07); 
  text-align: left;
  overflow: hidden; /* 确保子元素圆角生效 */
  transition: box-shadow 0.3s ease-in-out; /* 添加阴影过渡效果 */
}

.profile-info-group:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.09); /* 悬停时阴影更明显 */
}

.personal-info {
  display: flex;
  align-items: center;
  padding: 22px 24px; /* 略微增加内边距 */
  border-top: 1px solid #f5f5f5; /* 更淡的分割线 */
  cursor: pointer;
  transition: background-color 0.2s ease-in-out, transform 0.2s ease-in-out;
}

.personal-info:hover {
  background-color: #f9f9f9; /* 悬停背景色调整 */
  transform: none; /* 移除之前的translateX，让整体卡片阴影变化更突出 */
}

.personal-info:first-child {
  border-top: none;
}

.icon1 {
  font-size: 20px;
  color: #5a6a7b; /* 图标颜色微调 */
  margin-right: 22px; /* 略微增加与文字的间距 */
  width: 24px;
  text-align: center;
  transition: color 0.2s ease-in-out;
}

.personal-info:hover .icon1 {
  color: #3a4a5b; /* 悬停时图标颜色加深 */
}

.description {
  flex-grow: 1;
  font-size: 1.05rem; /* 略微增大字体 */
  color: #333;
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.1px;
}

.icon2 {
  font-size: 18px;
  color: #b0b8c0; /* 箭头图标颜色微调 */
  transition: color 0.2s ease-in-out, transform 0.2s ease-in-out;
}

.personal-info:hover .icon2 {
  color: #5a6a7b; /* 悬停时箭头颜色加深 */
  transform: translateX(3px); /* 悬停时箭头轻微右移 */
}

/* Removed styles for .account-actions, .action-button, .switch, .logout */
</style>