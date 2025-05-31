<template>
  <div class="account-management-page">
    <div class="page-header-container">
      <span class="back-icon" @click="goBack">
        <i class="fas fa-angle-left"></i>
      </span>
      <h2 class="title">账号管理</h2>
      <span class="placeholder-action"></span>
    </div>

    <div class="content-area">
      <div class="current-account-section" v-if="userStore.userProfile">
        <h3 class="section-title">当前账号</h3>
        <div class="account-card active-account">
          <img 
            :src="userStore.avatarUrl" 
            :alt="userStore.displayName" 
            class="account-avatar"
            @error="onAvatarError"
          />
          <div class="account-info">
            <p class="account-nickname">{{ userStore.displayName }}</p>
            <p class="account-username">@{{ userStore.userProfile.username }}</p>
          </div>
          <i class="fas fa-check-circle current-check"></i>
        </div>
      </div>
      <div v-else class="loading-placeholder">
        <p>加载用户信息...</p>
      </div>

      <div class="recent-accounts-section" v-if="otherRecentAccounts.length > 0">
        <h3 class="section-title">切换账号</h3>
        <div
          v-for="account in otherRecentAccounts"
          :key="account.username"
          class="account-card recent-account-item"
          @click="switchToAccount(account.username)"
        >
          <img
            :src="getDisplayAvatarUrl(account.avatarUrl, account.username)"  
            :alt="account.displayName"
            class="account-avatar"
            @error="onRecentAccountAvatarError($event, account)" 
          />
          <div class="account-info">
            <p class="account-nickname">{{ account.displayName }}</p>
            <p class="account-username">@{{ account.username }}</p>
          </div>
          <i class="fas fa-chevron-right switch-arrow"></i>
        </div>
      </div>

      <div class="add-account-section">
        <button class="add-account-button" @click="addAccount">
          <i class="fas fa-plus-circle icon-add"></i>
          添加账号
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { message, Modal as AModal } from 'ant-design-vue';
import { computed, reactive, nextTick } from 'vue'; // 引入 reactive 和 nextTick

const router = useRouter();
const userStore = useUserStore();

const defaultAvatarAssetUrl = new URL('@/assets/images/ProfilePortrait.jpg', import.meta.url).href;
const failedAvatarUsernames = reactive(new Set()); // 用于存储加载失败头像的用户名

// 改进头像 URL 处理
const getDisplayAvatarUrl = (storedUrl, username) => {
  if (username && failedAvatarUsernames.has(username)) {
    return defaultAvatarAssetUrl;
  }

  if (!storedUrl || storedUrl === 'DEFAULT_AVATAR') {
    return defaultAvatarAssetUrl;
  }
  
  // 假设 storedUrl 此时应该是一个完整的 HTTP/HTTPS URL (由 userStore 处理过)
  // 或者是一个需要进一步处理的路径 (尽管 userStore 应该已经处理了)
  try {
    // 验证是否是一个结构上有效的URL
    new URL(storedUrl); 
    return storedUrl;
  } catch (e) {
    // 如果 storedUrl 不是一个有效的完整URL (例如，它是一个相对路径或无效字符串)
    // 并且 userStore 没有正确地将其转换为完整URL，则尝试进一步处理或回退
    // 根据之前的逻辑，如果它以 '/' 开头，则尝试构造成本地服务器URL
    if (typeof storedUrl === 'string' && storedUrl.startsWith('/')) {
      // 这个逻辑分支可能可以简化，如果确信userStore总是提供完整URL或'DEFAULT_AVATAR'
      return `http://localhost:5000${storedUrl}`;
    }
    // 如果以上都不适用，说明URL有问题，标记为失败并使用默认头像
    if (username) {
      failedAvatarUsernames.add(username);
    }
    console.warn(`Malformed or unhandled avatar URL for ${username || 'unknown user'}: ${storedUrl}. Falling back to default.`);
    return defaultAvatarAssetUrl;
  }
};

const onRecentAccountAvatarError = (event, account) => {
  const username = account?.username;
  if (username) {
    console.warn(`Error loading avatar for recent account ${username}:`, event.target.src, ". Adding to failed list.");
    failedAvatarUsernames.add(username);
  } else {
    console.warn('Error loading avatar for recent account (unknown username):', event.target.src);
  }
  event.target.src = defaultAvatarAssetUrl;
  // 防止当前img元素因重复设置错误src而无限触发error事件
  event.target.onerror = null; 
};

const onAvatarError = (event) => {
  console.warn('Avatar load error for current user:', event.target.src);
  event.target.src = defaultAvatarAssetUrl;
  event.target.onerror = null;
};

const goBack = () => {
  router.push('/profile/personal');
};

const otherRecentAccounts = computed(() => {
  if (!userStore.userProfile) {
    return userStore.recentAccounts; // 如果当前没有登录用户，显示所有最近账户
  }
  return userStore.recentAccounts.filter(acc => acc.username !== userStore.userProfile.username);
});

const switchToAccount = (usernameToSwitch) => {
  if (userStore.userProfile && userStore.userProfile.username === usernameToSwitch) {
    message.info('您已登录此账号。');
    return;
  }

  AModal.confirm({
    title: '切换账号',
    content: `您确定要退出当前账号并尝试登录 ${usernameToSwitch} 吗？`,
    okText: '确定切换',
    cancelText: '取消',
    centered: true,
    width: '280px',    onOk: () => {
      // 清除用户数据
      userStore.clearUserProfile();
      
      // 使用setTimeout确保localStorage完全清除后再导航
      setTimeout(() => {
        // 再次确认token已被清除
        if (localStorage.getItem('token')) {
          localStorage.removeItem('token');
        }
        
        // 携带用户名到登录页，登录页可以尝试预填
        router.push({ path: '/login', query: { username: usernameToSwitch } }); 
        message.info(`请登录 ${usernameToSwitch}`);
      }, 100); // 100ms延迟确保所有操作完成
    },
  });
};

const addAccount = () => {
  AModal.confirm({
    title: '添加新账号',
    content: '您将会退出当前账号并跳转到登录页面，以添加新的账号。是否继续？',
    okText: '继续',
    cancelText: '取消',
    centered: true,
    width: '280px',
    onOk: () => {
      userStore.clearUserProfile();
      router.push('/login');
      message.info('请登录您的其他账号。');
    },
  });
};
</script>

<style scoped>
.account-management-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa; /* 修改为灰色背景 */
}

.page-header-container {
  display: flex;
  padding: 16px;
  align-items: center;
  background-color: #f8f9fa; /* 保持头部背景色与页面背景一致或设为白色，根据设计统一性决定 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
}

.back-icon {
  font-size: 22px;
  color: #333;
  cursor: pointer;
  padding: 8px;
  margin-right: 10px;
}

.back-icon:hover {
  color: #1e6fba;
}

.title {
  flex-grow: 1;
  text-align: center;
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #333;
}
.placeholder-action {
  width: 40px; 
}

.content-area {
  padding: 20px;
  flex-grow: 1;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
  margin-top: 20px; /* Add margin top for sections other than the first */
}
.current-account-section .section-title {
  margin-top: 0; /* No top margin for the very first section title */
}


.account-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: #fff; /* 修改为白色背景 */
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  margin-bottom: 12px; /* Space between cards */
  position: relative; /* For absolute positioning of icons */
}

.account-card.active-account {
  border: 2px solid #007bff; /* Highlight active account */
  /* background-color: #fff; 确保激活状态也是白底 */
}

.recent-account-item {
  cursor: pointer;
  transition: background-color 0.2s ease;
  /* background-color: #fff; 确保初始为白底 */
}
.recent-account-item:hover {
  background-color: #e9ecef; /* 悬停时背景色可以保持或调整为更浅的灰色 */
}


.account-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 16px;
  border: 2px solid #fff; /* Optional: white border around avatar */
}

.account-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Allow info to take available space */
}

.account-nickname {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin: 0 0 2px 0;
}

.account-username {
  font-size: 0.85rem;
  color: #6c757d;
  margin: 0;
}

.current-check {
  color: #28a745; /* Green check for current account */
  font-size: 1.2em;
  margin-left: auto; /* Push to the right */
  padding-left: 10px;
}

.switch-arrow {
  color: #6c757d; /* Arrow color for switchable accounts */
  font-size: 1em;
  margin-left: auto; /* Push to the right */
  padding-left: 10px;
}


.add-account-section {
  margin-top: 30px; /* More space before add button */
}

.add-account-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 14px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.add-account-button:hover {
  background-color: #0056b3;
}
.add-account-button:active {
  transform: scale(0.98);
}

.icon-add {
  margin-right: 8px;
  font-size: 1.1em;
}

.loading-placeholder {
  text-align: center;
  padding: 20px;
  color: #6c757d;
}
</style>