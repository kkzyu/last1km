<template>
  <HomeHead />
  <div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="input-group">
        <span class="input-label">用户名 *</span>
        <input 
          type="text" 
          v-model="username" 
          placeholder="请输入用户名（3-80个字符）" 
          required
          maxlength="80"
        >
      </div>
      <div class="input-group">
        <span class="input-label">昵称</span>
        <input 
          type="text" 
          v-model="nickname" 
          placeholder="请输入昵称（可选）"
          maxlength="100"
        >
      </div>
      <div class="input-group">
        <span class="input-label">手机号</span>
        <input 
          type="tel" 
          v-model="phone" 
          placeholder="请输入手机号（可选）"
          pattern="1[3-9]\d{9}"
        >
      </div>
      <div class="input-group">
        <span class="input-label">邮箱</span>
        <input 
          type="email" 
          v-model="email" 
          placeholder="请输入邮箱（可选）"
          maxlength="120"
        >
      </div>
      
      <!-- 密码输入框增强 -->
      <div class="input-group">
        <span class="input-label">密码 *</span>
        <div class="password-input-container">
          <input 
            :type="showPassword ? 'text' : 'password'"
            v-model="password" 
            placeholder="请输入密码（至少6位）" 
            required
            minlength="6"
            @input="checkPasswordStrength"
          >
          <button 
            type="button" 
            class="password-toggle" 
            @click="togglePasswordVisibility"
            :title="showPassword ? '隐藏密码' : '显示密码'"
          >
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>
        
        <!-- 密码强度指示器 -->
        <div v-if="password" class="password-strength">
          <div class="strength-bar">
            <div 
              class="strength-fill" 
              :class="`strength-${passwordStrength.level}`"
              :style="{ width: passwordStrength.percentage + '%' }"
            ></div>
          </div>
          <div class="strength-text" :class="`strength-${passwordStrength.level}`">
            {{ passwordStrength.text }}
          </div>
          
          <!-- 密码要求提示 -->
          <div class="password-requirements">
            <div class="requirement" :class="{ met: passwordChecks.length }">
              <i class="fas fa-check" v-if="passwordChecks.length"></i>
              <i class="fas fa-times" v-else></i>
              至少6个字符
            </div>
            <div class="requirement" :class="{ met: passwordChecks.hasUpperCase }">
              <i class="fas fa-check" v-if="passwordChecks.hasUpperCase"></i>
              <i class="fas fa-times" v-else></i>
              包含大写字母
            </div>
            <div class="requirement" :class="{ met: passwordChecks.hasLowerCase }">
              <i class="fas fa-check" v-if="passwordChecks.hasLowerCase"></i>
              <i class="fas fa-times" v-else></i>
              包含小写字母
            </div>
            <div class="requirement" :class="{ met: passwordChecks.hasNumber }">
              <i class="fas fa-check" v-if="passwordChecks.hasNumber"></i>
              <i class="fas fa-times" v-else></i>
              包含数字
            </div>
            <div class="requirement" :class="{ met: passwordChecks.hasSpecial }">
              <i class="fas fa-check" v-if="passwordChecks.hasSpecial"></i>
              <i class="fas fa-times" v-else></i>
              包含特殊字符
            </div>
          </div>
        </div>
      </div>
      
      <!-- 确认密码输入框增强 -->
      <div class="input-group">
        <span class="input-label">确认密码 *</span>
        <div class="password-input-container">
          <input 
            :type="showConfirmPassword ? 'text' : 'password'"
            v-model="confirmPassword" 
            placeholder="请再次输入密码" 
            required
            minlength="6"
          >
          <button 
            type="button" 
            class="password-toggle" 
            @click="toggleConfirmPasswordVisibility"
            :title="showConfirmPassword ? '隐藏密码' : '显示密码'"
          >
            <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>
        
        <!-- 密码匹配提示 -->
        <div v-if="confirmPassword" class="password-match">
          <div v-if="password === confirmPassword" class="match-success">
            <i class="fas fa-check"></i>
            密码匹配
          </div>
          <div v-else class="match-error">
            <i class="fas fa-times"></i>
            密码不匹配
          </div>
        </div>
      </div>
      
      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="success" class="success-message">{{ success }}</p>
      
      <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
        {{ loading ? '注册中...' : '注册' }}
      </button>
      
      <button type="button" @click="goToLogin" class="btn btn-secondary" :disabled="loading">
        返回登录
      </button>
    </form>
    
    <p class="navigation-link">
      已有账号？<a @click="goToLogin" class="link-text">立即登录</a>
    </p>
  </div>
  <BottomNav />
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'
import { register } from '@/api/auth.js'

const router = useRouter();
const username = ref('');
const nickname = ref('');
const phone = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref('');
const success = ref('');

// 密码可见性控制
const showPassword = ref(false);
const showConfirmPassword = ref(false);

// 密码强度检测
const passwordStrength = ref({
  level: 'weak',
  percentage: 0,
  text: '弱'
});

const passwordChecks = ref({
  length: false,
  hasUpperCase: false,
  hasLowerCase: false,
  hasNumber: false,
  hasSpecial: false
});

// 计算表单是否有效
const isFormValid = computed(() => {
  return username.value.trim().length >= 3 &&
         password.value.length >= 6 &&
         confirmPassword.value.length >= 6 &&
         password.value === confirmPassword.value &&
         passwordStrength.value.level !== 'weak' &&
         (!phone.value.trim() || /^1[3-9]\d{9}$/.test(phone.value.trim())) &&
         (!email.value.trim() || /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.value.trim()));
});

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

// 检查密码强度
const checkPasswordStrength = () => {
  const pwd = password.value;
  
  // 重置检查项
  passwordChecks.value = {
    length: pwd.length >= 6,
    hasUpperCase: /[A-Z]/.test(pwd),
    hasLowerCase: /[a-z]/.test(pwd),
    hasNumber: /\d/.test(pwd),
    hasSpecial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(pwd)
  };
  
  // 计算强度分数
  let score = 0;
  if (passwordChecks.value.length) score += 20;
  if (passwordChecks.value.hasLowerCase) score += 20;
  if (passwordChecks.value.hasUpperCase) score += 20;
  if (passwordChecks.value.hasNumber) score += 20;
  if (passwordChecks.value.hasSpecial) score += 20;
  
  // 额外加分：长度超过8位
  if (pwd.length >= 8) score += 10;
  if (pwd.length >= 12) score += 10;
  
  // 确定强度等级
  if (score < 40) {
    passwordStrength.value = { level: 'weak', percentage: score, text: '弱' };
  } else if (score < 70) {
    passwordStrength.value = { level: 'medium', percentage: score, text: '中等' };
  } else if (score < 90) {
    passwordStrength.value = { level: 'strong', percentage: score, text: '强' };
  } else {
    passwordStrength.value = { level: 'very-strong', percentage: score, text: '很强' };
  }
};

const validateForm = () => {
  // 清除之前的错误信息
  error.value = '';
  
  // 验证必填字段
  if (!username.value.trim()) {
    error.value = '请输入用户名！';
    return false;
  }
  
  if (!password.value) {
    error.value = '请输入密码！';
    return false;
  }
  
  if (!confirmPassword.value) {
    error.value = '请确认密码！';
    return false;
  }
  
  // 验证用户名格式
  if (username.value.trim().length < 3 || username.value.trim().length > 80) {
    error.value = '用户名长度必须在3-80个字符之间！';
    return false;
  }
  
  if (!/^[a-zA-Z0-9_]+$/.test(username.value.trim())) {
    error.value = '用户名只能包含字母、数字和下划线！';
    return false;
  }
  
  // 验证密码
  if (password.value.length < 6) {
    error.value = '密码长度不能少于6位！';
    return false;
  }
  
  if (passwordStrength.value.level === 'weak') {
    error.value = '密码强度太弱，请设置更复杂的密码！';
    return false;
  }
  
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致！';
    return false;
  }
  
  // 验证手机号（如果填写了）
  if (phone.value.trim() && !/^1[3-9]\d{9}$/.test(phone.value.trim())) {
    error.value = '请输入正确的手机号格式！';
    return false;
  }
  
  // 验证邮箱（如果填写了）
  if (email.value.trim() && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.value.trim())) {
    error.value = '请输入正确的邮箱格式！';
    return false;
  }
  
  return true;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  error.value = '';
  success.value = '';

  try {
    const userData = {
      username: username.value.trim(),
      password: password.value,
      nickname: nickname.value.trim() || username.value.trim(),
      phone: phone.value.trim() || '',
      email: email.value.trim() || '',
    };

    const response = await register(userData);
    
    if (response.code === 200) {
      success.value = '注册成功！即将跳转到登录页面...';
      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } else {
      error.value = response.message || '注册失败，请重试。';
    }
  } catch (err) {
    console.error('注册失败:', err);
    error.value = err.message || '注册失败，请检查网络连接。';
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  if (loading.value) return;
  router.push('/login');
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
  margin: 40px auto;
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

/* 密码输入容器 */
.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-container input {
  flex: 1;
  padding-right: 45px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #4a90e2;
}

input[type="text"],
input[type="email"],
input[type="tel"],
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
input[type="email"]:focus,
input[type="tel"]:focus,
input[type="password"]:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 10px;
}

.strength-bar {
  width: 100%;
  height: 4px;
  background-color: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.strength-fill {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-weak { background-color: #ff4444; }
.strength-medium { background-color: #ff8800; }
.strength-strong { background-color: #44ff44; }
.strength-very-strong { background-color: #00aa00; }

.strength-text {
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 8px;
}

.strength-text.strength-weak { color: #ff4444; }
.strength-text.strength-medium { color: #ff8800; }
.strength-text.strength-strong { color: #44ff44; }
.strength-text.strength-very-strong { color: #00aa00; }

/* 密码要求 */
.password-requirements {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-top: 8px;
}

.requirement {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #999;
  transition: color 0.2s;
}

.requirement.met {
  color: #27ae60;
}

.requirement i {
  margin-right: 6px;
  width: 10px;
}

/* 密码匹配指示器 */
.password-match {
  margin-top: 8px;
  font-size: 12px;
}

.match-success {
  color: #27ae60;
  display: flex;
  align-items: center;
}

.match-error {
  color: #e74c3c;
  display: flex;
  align-items: center;
}

.match-success i,
.match-error i {
  margin-right: 6px;
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
  color: #52c41a;
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

/* 响应式设计 */
@media (max-width: 480px) {
  .password-requirements {
    grid-template-columns: 1fr;
  }
  
  .auth-container {
    width: 95%;
    padding: 20px 15px;
  }
}
</style>