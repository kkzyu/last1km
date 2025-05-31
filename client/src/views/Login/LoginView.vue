<template>
  <HomeHead />
  <div class="auth-container">
    <h2>密码登录</h2>
    <form @submit.prevent="handleLogin"> 
      <div class="input-group">
        <span class="input-label">昵称</span>
        <input type="text" v-model="username" placeholder="请输入用户名称" required> 
      </div>
      <div class="input-field-only">
        <input type="password" v-model="password" placeholder="请输入密码" required>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <button type="button" @click="goToRegister" class="btn btn-secondary" :disabled="loading">注册</button> 
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </form>
  </div>
  <BottomNav />
</template>

<script setup>
import { ref, onMounted } from 'vue'; // Import onMounted
import { useRouter, useRoute } from 'vue-router'; // Import useRoute
import { authAPI } from '@/api/api';
import { useUserStore } from '@/stores/userStore'; // 导入 userStore
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

const router = useRouter();
const route = useRoute(); // Get current route
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const formState = ref({
  username: '',
  password: '',
  remember: true,
});

onMounted(() => {
  if (route.query.username) {
    formState.value.username = route.query.username;
  }
});

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码！';
    return;
  }

  loading.value = true;
  error.value = ''; // 清除之前的错误

  try {
    const response = await authAPI.login({
      username: username.value,
      password: password.value
    });

    if (response.data.success) {
      // 使用 userStore.loginSuccess 存储认证信息和用户数据
      userStore.loginSuccess(response.data.data.token, response.data.data.user);

      // 跳转逻辑
      const redirectPath = route.query.redirect || { name: 'home' };
      router.push(redirectPath);
    }
  } catch (err) {
    error.value = err.message || '登录失败，请重试。';
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  if (loading.value) return; // 防止在登录请求时跳转
  router.push('/register');
};
</script>

<style scoped>
.auth-container {
  background-color: #ffffff;
  padding: 30px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  width: 340px;
  max-width: 90%;
  margin: 60px auto;
  text-align: center;
}

h2 {
  font-size: 26px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.input-group {
  margin-bottom: 24px;
  text-align: left;
}

.input-field-only {
  margin-bottom: 24px;
}

.input-label {
  display: block;
  font-size: 15px;
  color: #666;
  margin-bottom: 8px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  box-sizing: border-box;
  outline: none;
  transition: all 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
}

.btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  /* display: block; /* 如果希望按钮独占一行 */
  /* margin-top: 10px; /* 如果按钮是 block，可以加点间距 */
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
  margin-top: 10px; /* 给登录按钮一点上边距，如果注册按钮在它上方 */
}

.btn-primary:hover:not(:disabled) { /* 仅在未禁用时应用 hover 效果 */
  background-color: #357abd;
  transform: translateY(-1px);
}

.btn-primary:disabled { /* 禁用时的样式 */
  background-color: #a0c7e8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
  margin-bottom: 12px; /* 与原样式保持一致 */
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e8e8e8;
}

.btn-secondary:disabled {
  background-color: #e0e0e0;
  color: #aaa;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: left; /* 或者 center，根据你的设计 */
}
</style>