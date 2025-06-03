<template>
  <div class="page-wrapper">
    <div class="scrollable-content">
      <HomeHead />
      <div class="auth-container">
        <h2>注册</h2>
        <form @submit.prevent="handleRegister">
          <div class="input-group">
            <span class="input-label">昵称</span>
            <input type="text" v-model="username" placeholder="请输入用户名称" required>
          </div>
          <div class="input-group">
            <span class="input-label">手机号</span>
            <input type="text" v-model="phoneNumber" placeholder="请输入手机号" required>
          </div>
          <div class="input-field-only">
            <input 
              type="password" 
              v-model="password" 
              placeholder="请输入密码" 
              required 
              @input="validatePasswordRealtime"
              @focus="passwordFocused = true"
            >
          </div>
        
        <!-- 美化的密码强度提示 -->
        <div v-if="passwordFocused || password.length > 0" class="password-strength-container">
          <div class="strength-header">
            <span class="strength-title">密码强度</span>
            <div class="strength-bar">
              <div class="strength-progress" :style="{ width: strengthPercentage + '%' }" :class="strengthClass"></div>
            </div>
            <span class="strength-text" :class="strengthClass">{{ strengthText }}</span>
          </div>
          
          <div class="criteria-list">
            <div class="criteria-row">
              <div class="criteria-item" :class="{ 'satisfied': passwordChecks.length }">
                <div class="criteria-icon">
                  <i class="icon" :class="passwordChecks.length ? 'icon-check' : 'icon-close'"></i>
                </div>
                <span class="criteria-text">长度至少为8位</span>
              </div>
              
              <div class="criteria-item" :class="{ 'satisfied': passwordChecks.lowercase }">
                <div class="criteria-icon">
                  <i class="icon" :class="passwordChecks.lowercase ? 'icon-check' : 'icon-close'"></i>
                </div>
                <span class="criteria-text">包含小写字母</span>
              </div>
            </div>
            
            <div class="criteria-row">
              <div class="criteria-item" :class="{ 'satisfied': passwordChecks.uppercase }">
                <div class="criteria-icon">
                  <i class="icon" :class="passwordChecks.uppercase ? 'icon-check' : 'icon-close'"></i>
                </div>
                <span class="criteria-text">包含大写字母</span>
              </div>
              
              <div class="criteria-item" :class="{ 'satisfied': passwordChecks.digit }">
                <div class="criteria-icon">
                  <i class="icon" :class="passwordChecks.digit ? 'icon-check' : 'icon-close'"></i>
                </div>
                <span class="criteria-text">包含数字</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-field-only">
          <input type="password" v-model="confirmPassword" placeholder="请确认密码" required>
        </div>
        <p v-if="error" class="error-message">{{ error }}</p>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>        <p class="navigation-link">
          已有账号？<a @click="goToLogin">立即登录</a>
        </p>
      </form>
    </div>
    </div>
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '@/api/api';
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

const router = useRouter();
const username = ref('');
const phoneNumber = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref('');
const passwordFocused = ref(false);

// Reactive object for password strength checks
const passwordChecks = reactive({
  length: false,
  lowercase: false,
  uppercase: false,
  digit: false,
});

// 计算密码强度百分比
const strengthPercentage = computed(() => {
  const satisfied = Object.values(passwordChecks).filter(Boolean).length;
  return (satisfied / 4) * 100;
});

// 计算密码强度等级
const strengthLevel = computed(() => {
  const satisfied = Object.values(passwordChecks).filter(Boolean).length;
  if (satisfied === 0) return 0;
  if (satisfied <= 1) return 1; // 弱
  if (satisfied <= 2) return 2; // 中等
  if (satisfied <= 3) return 3; // 强
  return 4; // 很强
});

// 计算强度文本
const strengthText = computed(() => {
  const level = strengthLevel.value;
  const texts = ['', '弱', '中等', '强', '很强'];
  return texts[level];
});

// 计算强度样式类
const strengthClass = computed(() => {
  const level = strengthLevel.value;
  const classes = ['', 'weak', 'fair', 'good', 'strong'];
  return classes[level];
});

const validatePasswordRealtime = () => {
  const p = password.value;
  passwordChecks.length = p.length >= 8;
  passwordChecks.lowercase = /[a-z]/.test(p);
  passwordChecks.uppercase = /[A-Z]/.test(p);
  passwordChecks.digit = /\d/.test(p);
};

// Watch for changes in the password field to validate in real-time
watch(password, validatePasswordRealtime);

const handleRegister = async () => {
  if (!username.value || !phoneNumber.value || !password.value || !confirmPassword.value) {
    error.value = '请填写所有注册信息！';
    return;
  }
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致！';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    await authAPI.register({
      username: username.value,
      password: password.value,
      phone: phoneNumber.value
    });
    router.push('/login');
  } catch (err) {
    error.value = err.message || '注册失败，请重试';
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
/* 页面整体包装器 */
.page-wrapper {
  height: 100vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f7;
}

/* 可滚动内容区域 */
.scrollable-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: 60px; /* 为BottomNav留出空间 */
  
  /* 隐藏滚动条 - Webkit浏览器 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE和Edge */
}

.scrollable-content::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

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

/* 美化的密码强度容器 */
.password-strength-container {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid #dee2e6;
  border-radius: 12px;
  padding: 16px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.password-strength-container:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 强度头部 */
.strength-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.strength-title {
  font-size: 13px;
  font-weight: 600;
  color: #495057;
  min-width: 60px;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background-color: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}

.strength-progress {
  height: 100%;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 3px;
}

.strength-progress.weak {
  background: linear-gradient(90deg, #dc3545, #e74c3c);
}

.strength-progress.fair {
  background: linear-gradient(90deg, #fd7e14, #ff8c00);
}

.strength-progress.good {
  background: linear-gradient(90deg, #ffc107, #ffcd39);
}

.strength-progress.strong {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.strength-text {
  font-size: 12px;
  font-weight: 600;
  min-width: 40px;
  text-align: right;
}

.strength-text.weak { color: #dc3545; }
.strength-text.fair { color: #fd7e14; }
.strength-text.good { color: #ffc107; }
.strength-text.strong { color: #28a745; }

/* 条件列表 */
.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.criteria-row {
  display: flex;
  gap: 8px;
}

.criteria-item {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.criteria-item.satisfied {
  background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(32, 201, 151, 0.1));
  border-color: rgba(40, 167, 69, 0.2);
  transform: translateX(2px);
}

.criteria-item:not(.satisfied) {
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.05), rgba(231, 76, 60, 0.05));
  border-color: rgba(220, 53, 69, 0.1);
}

.criteria-icon {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.criteria-item.satisfied .criteria-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.criteria-item:not(.satisfied) .criteria-icon {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.2);
}

.icon {
  font-size: 10px;
  font-weight: bold;
  color: white;
}

.icon-check::before {
  content: '✓';
}

.icon-close::before {
  content: '✗';
}

.criteria-text {
  font-size: 12px;
  font-weight: 500;
  transition: color 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.criteria-item.satisfied .criteria-text {
  color: #155724;
}

.criteria-item:not(.satisfied) .criteria-text {
  color: #721c24;
}

/* 错误消息样式 */
.error-message {
  color: #dc3545;
  font-size: 14px;
  margin: 10px 0;
  padding: 10px;
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
  border-radius: 6px;
  text-align: center;
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

.btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  transform: none;
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