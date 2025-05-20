<template>
  <HomeHead />
  <div class="auth-container">
    <h2>注册</h2>
    <div class="input-group">
      <span class="input-label">昵称</span>
      <input type="text" v-model="username" placeholder="请输入用户名称">
    </div>
    <div class="input-group">
      <span class="input-label">手机号</span>
      <input type="text" v-model="phoneNumber" placeholder="请输入手机号">
    </div>
    <div class="input-field-only">
      <input type="password" v-model="password" placeholder="请输入密码">
    </div>
    <div class="input-field-only">
      <input type="password" v-model="confirmPassword" placeholder="请确认密码">
    </div>
    <button @click="handleRegister" class="btn btn-primary">注册</button>
    <p class="navigation-link">
      已有账号？<a @click="goToLogin">立即登录</a>
    </p>
  </div>
  <BottomNav />
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

const router = useRouter();
const username = ref('');
const phoneNumber = ref('');
const password = ref('');
const confirmPassword = ref('');

const handleRegister = () => {
  if (!username.value || !phoneNumber.value || !password.value || !confirmPassword.value) {
    alert('请填写所有注册信息！');
    return;
  }
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致！');
    return;
  }
  // 模拟注册成功
  alert('注册成功！将跳转到登录页面。');
  router.push('/'); // 注册成功后跳转到登录页
};

const goToLogin = () => {
  router.push('/login'); // 更新为新的登录路径
};
</script>

<style scoped>
.auth-container {
  background-color: #ffffff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  width: 340px;
  max-width: 90%;
  margin: 40px auto;
  text-align: center;
}

h2 {
  font-size: 26px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.input-group,
.input-field-only {
  margin-bottom: 20px;
  text-align: left;
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
  color: white;
  background-color: #4a90e2;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn:hover {
  background-color: #357abd;
  transform: translateY(-1px);
}

.navigation-link {
  margin-top: 24px;
  font-size: 15px;
  color: #666;
}

.navigation-link a {
  color: #4a90e2;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
  margin-left: 5px;
}

.navigation-link a:hover {
  text-decoration: underline;
  color: #357abd;
}
</style>