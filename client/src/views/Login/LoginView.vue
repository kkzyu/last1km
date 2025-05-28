<template>
  <HomeHead />
  <div class="auth-container">
    <h2>密码登录</h2>
    <form @submit.prevent="handleLogin"> 
      <div class="input-group">
        <span class="input-label">用户名 *</span>
        <input 
          type="text" 
          v-model="username" 
          placeholder="请输入用户名" 
          required
          maxlength="80"
        > 
      </div>
      <div class="input-group">
        <span class="input-label">密码 *</span>
        <input 
          type="password" 
          v-model="password" 
          placeholder="请输入密码" 
          required
          minlength="6"
        >
      </div>
      
      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="success" class="success-message">{{ success }}</p>
      
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
      
      <button type="button" @click="goToRegister" class="btn btn-secondary" :disabled="loading">
        注册新账户
      </button>
    </form>
    
    <p class="navigation-link">
      没有账号？<a @click="goToRegister" class="link-text">立即注册</a>
    </p>
  </div>
  <BottomNav />
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'
import { login } from '@/api/auth.js'

const router = useRouter();
const route = useRoute();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');
const success = ref('');

const validateForm = () => {
  error.value = '';
  
  if (!username.value.trim()) {
    error.value = '请输入用户名！';
    return false;
  }
  
  if (!password.value) {
    error.value = '请输入密码！';
    return false;
  }
  
  if (password.value.length < 6) {
    error.value = '密码长度不能少于6位！';
    return false;
  }
  
  return true;
};

const handleLogin = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  error.value = '';
  success.value = '';

  try {
    const credentials = {
      username: username.value.trim(),
      password: password.value,
    };

    const response = await login(credentials);

    if (response.code === 200) {
      // 存储认证信息
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('userInfo', JSON.stringify(response.data.user));

      success.value = '登录成功！正在跳转...';
      
      // 延迟跳转，让用户看到成功消息
      setTimeout(() => {
        const redirectPath = route.query.redirect || '/';
        router.push(redirectPath);
      }, 1000);
    } else {
      error.value = response.message || '登录失败，请重试。';
    }
  } catch (err) {
    console.error('登录失败:', err);
    error.value = err.response?.data?.message || err.message || '登录失败，请检查网络连接。';
  } finally {
    loading.value = false;
  }
};

const goToRegister = () => {
  if (loading.value) return;
  router.push('/register');
};
</script>

<style scoped>
.auth-container {
  background-color: #ffffff;
  padding: 30px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  width: 380px;
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
  margin-bottom: 20px;
  text-align: left;
}

.input-label {
  display: block;
  font-size: 15px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
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
  margin-bottom: 12px;
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #357abd;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background-color: #a0c7e8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
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
  color: #e74c3c;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: left;
  padding: 8px 12px;
  background-color: #fdf2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.success-message {
  color: #27ae60;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: left;
  padding: 8px 12px;
  background-color: #f0f9f0;
  border: 1px solid #86efac;
  border-radius: 6px;
}

.navigation-link {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.link-text {
  color: #4a90e2;
  cursor: pointer;
  text-decoration: none;
  font-weight: 500;
}

.link-text:hover {
  color: #357abd;
  text-decoration: underline;
}
</style>