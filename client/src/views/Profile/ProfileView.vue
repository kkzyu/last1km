<template>
  <div class="page-container">
    <ProfilePortrait 
      :username="userStore.displayName"
      :avatarUrl="userStore.avatarUrl"
      :gender="userStore.gender"
    />
    <div class="profile-info">
      <div class="personal-info">
        <span class="icon1"><i class="fas fa-address-card"></i></span>
        <p class="description">个人资料</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="navigateTo('/profile/personal')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fa fa-google-wallet"></i></span> <p class="description">钱包/优惠券</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="navigateTo('/profile/wallet')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fas fa-bars"></i></span>
        <p class="description">历史订单</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="navigateTo('/profile/orders')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fas fa-headphones"></i></span>
        <p class="description">联系客服</p>
        <span class="icon2"><i class="fas fa-angle-right"></i></span> </div>

      <div class="personal-info last-info">
        <span class="icon1"><i class="fas fa-certificate"></i></span>
        <p class="description">设置</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="navigateTo('/profile/settings')"></i></span>
      </div>
    </div>

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
  background-color: #F7F8FA;
  padding: 20px;
  padding-bottom: 80px; /* 为 BottomNav 留出空间 */
  min-height: calc(100vh - 80px); /* 考虑 BottomNav 的高度 */
  box-sizing: border-box;
  /* text-align: center; // 从父级移除，让 ProfilePortrait 自己控制对齐 */
}

.profile-info {
  background-color: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
  text-align: left;
}

.personal-info {
  display: flex;
  align-items: center;
  padding: 18px 20px;
  border-top: 1px solid #F0F0F0;
  cursor: pointer; /* 使整个条目可点击 */
}
.personal-info:hover {
  background-color: #f9f9f9;
}

.personal-info:first-child {
  border-top: none;
}

.last-info {
  /* 样式可以保持或移除，如果不再有特殊处理 */
}

.icon1 {
  font-size: 20px; /* 略微调整图标大小 */
  color: #5D6D7E;
  margin-right: 18px;
  width: 24px; /* 固定宽度方便对齐 */
  text-align: center;
}

.description {
  flex-grow: 1;
  font-size: 1rem;
  color: #34495E;
  margin: 0;
}

.icon2 {
  font-size: 18px; /* 略微调整图标大小 */
  color: #AEB6BF;
  /* cursor: pointer; // 已移到 .personal-info */
  transition: color 0.2s ease-in-out;
}

/* .icon2:hover { // 效果现在由 .personal-info:hover 控制
  color: #5D6D7E;
} */

/* Removed styles for .account-actions, .action-button, .switch, .logout */
</style>