<template>
  <div class="profile-personal">
    <!-- 顶部导航 -->
    <div class="page-header">
      <span class="back-icon" @click="$router.push('/profile')">
        <i class="fas fa-angle-left"></i>
      </span>
      <h2 class="title">个人资料</h2>
      <span class="save-btn" @click="saveProfile" :class="{ disabled: saving }">
        {{ saving ? '保存中...' : '保存' }}
      </span>
    </div>

    <!-- 头像部分 -->
    <div class="avatar-section">
      <div class="avatar-container" @click="selectAvatar">
        <img 
          :src="profileForm.avatar || defaultAvatarUrl" 
          alt="头像" 
          class="avatar"
          @error="handleAvatarError"
        />
        <div class="avatar-overlay">
          <i class="fas fa-camera"></i>
        </div>
      </div>
      <input 
        ref="avatarInput" 
        type="file" 
        accept="image/*" 
        @change="handleAvatarChange" 
        style="display: none"
      />
    </div>

    <!-- 表单部分 -->
    <div class="form-section">
      <div class="form-group">
        <label class="form-label">用户名</label>
        <div class="form-value readonly">{{ profileForm.username || '未设置' }}</div>
        <span class="form-note">用户名不可修改</span>
      </div>

      <div class="form-group">
        <label class="form-label">昵称</label>
        <input 
          type="text" 
          class="form-input" 
          v-model="profileForm.nickname" 
          placeholder="请输入昵称"
          maxlength="100"
        />
      </div>

      <div class="form-group">
        <label class="form-label">性别</label>
        <div class="gender-options">
          <label class="gender-option">
            <input type="radio" v-model="profileForm.gender" value="male" />
            <span class="gender-text">男</span>
          </label>
          <label class="gender-option">
            <input type="radio" v-model="profileForm.gender" value="female" />
            <span class="gender-text">女</span>
          </label>
          <label class="gender-option">
            <input type="radio" v-model="profileForm.gender" value="" />
            <span class="gender-text">不透露</span>
          </label>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">手机号</label>
        <input 
          type="tel" 
          class="form-input" 
          v-model="profileForm.phone" 
          placeholder="请输入手机号"
          pattern="1[3-9]\d{9}"
        />
      </div>

      <div class="form-group">
        <label class="form-label">邮箱</label>
        <input 
          type="email" 
          class="form-input" 
          v-model="profileForm.email" 
          placeholder="请输入邮箱"
          maxlength="120"
        />
      </div>
    </div>

    <!-- 配送地址设置 -->
    <div class="address-section">
      <div class="section-header">
        <h3>配送地址设置</h3>
        <span class="section-note">设置常用的取餐和送达地址</span>
      </div>
      
      <div class="address-group">
        <div class="address-item" @click="goToAddressManagement('pickup')">
          <div class="address-content">
            <div class="address-label">
              <i class="fas fa-store"></i>
              <span>默认取餐地址</span>
            </div>
            <div class="address-text">
              {{ profileForm.default_pickup_address || '点击设置取餐地址' }}
            </div>
          </div>
          <i class="fas fa-angle-right"></i>
        </div>
        
        <div class="address-item" @click="goToAddressManagement('delivery')">
          <div class="address-content">
            <div class="address-label">
              <i class="fas fa-map-marker-alt"></i>
              <span>默认送达地址</span>
            </div>
            <div class="address-text">
              {{ profileForm.default_delivery_address || '点击设置送达地址' }}
            </div>
          </div>
          <i class="fas fa-angle-right"></i>
        </div>
      </div>
    </div>

    <!-- 错误和成功消息 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <!-- 其他操作 -->
    <div class="action-section">
      <div class="action-item" @click="showChangePasswordModal">
        <span class="action-text">修改密码</span>
        <i class="fas fa-angle-right"></i>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="changePasswordVisible" class="modal-overlay" @click="closeChangePasswordModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>修改密码</h3>
          <span class="close-btn" @click="closeChangePasswordModal">&times;</span>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">当前密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.oldPassword" 
              placeholder="请输入当前密码"
            />
          </div>
          <div class="form-group">
            <label class="form-label">新密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.newPassword" 
              placeholder="请输入新密码（至少6位）"
              minlength="6"
            />
          </div>
          <div class="form-group">
            <label class="form-label">确认新密码</label>
            <input 
              type="password" 
              class="form-input" 
              v-model="passwordForm.confirmPassword" 
              placeholder="请再次输入新密码"
            />
          </div>
          <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeChangePasswordModal">取消</button>
          <button class="btn btn-primary" @click="changePassword" :disabled="changingPassword">
            {{ changingPassword ? '修改中...' : '确认修改' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getUserProfile, updateUserProfile, changePassword as changePasswordAPI, uploadAvatar } from '@/api/auth.js';

const router = useRouter();

// 生成默认头像URL
const defaultAvatarUrl = computed(() => {
  return `${import.meta.env.BASE_URL}images/ProfilePortrait.jpg`;
});

const profileForm = ref({
  id: null,
  username: '',
  nickname: '',
  avatar: '',
  gender: '',
  phone: '',
  email: '',
  default_pickup_address: '',
  default_delivery_address: ''
});

const saving = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const avatarInput = ref(null);

// 修改密码相关
const changePasswordVisible = ref(false);
const changingPassword = ref(false);
const passwordError = ref('');
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

onMounted(async () => {
  await loadUserProfile();
});

const loadUserProfile = async () => {
  try {
    // 先从localStorage获取缓存数据
    const cachedUserInfo = localStorage.getItem('userInfo');
    if (cachedUserInfo) {
      const userInfo = JSON.parse(cachedUserInfo);
      profileForm.value = { ...profileForm.value, ...userInfo };
    }

    // 检查是否有token
    const token = localStorage.getItem('authToken');
    if (!token) {
      errorMessage.value = '请先登录';
      setTimeout(() => {
        router.push('/login');
      }, 2000);
      return;
    }

    // 尝试从API获取最新数据
    const response = await getUserProfile();
    if (response.code === 200) {
      profileForm.value = { ...profileForm.value, ...response.data.user };
      // 更新localStorage缓存
      localStorage.setItem('userInfo', JSON.stringify(response.data.user));
    }
  } catch (error) {
    console.error('获取用户资料失败:', error);
    // 如果API调用失败，但有缓存数据，则使用缓存数据
    if (!profileForm.value.username) {
      errorMessage.value = '获取用户资料失败，请检查网络连接';
    }
  }
};

const saveProfile = async () => {
  if (saving.value) return;
  
  errorMessage.value = '';
  successMessage.value = '';
  
  // 验证表单
  if (!profileForm.value.nickname?.trim()) {
    errorMessage.value = '昵称不能为空';
    return;
  }
  
  if (profileForm.value.phone && !/^1[3-9]\d{9}$/.test(profileForm.value.phone)) {
    errorMessage.value = '请输入正确的手机号格式';
    return;
  }
  
  if (profileForm.value.email && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(profileForm.value.email)) {
    errorMessage.value = '请输入正确的邮箱格式';
    return;
  }
  
  saving.value = true;
  
  try {
    const updateData = {
      nickname: profileForm.value.nickname.trim(),
      gender: profileForm.value.gender,
      phone: profileForm.value.phone.trim(),
      email: profileForm.value.email.trim(),
      default_pickup_address: profileForm.value.default_pickup_address.trim(),
      default_delivery_address: profileForm.value.default_delivery_address.trim()
    };
    
    const response = await updateUserProfile(updateData);
    
    if (response.code === 200) {
      successMessage.value = '保存成功';
      // 更新localStorage中的用户信息
      localStorage.setItem('userInfo', JSON.stringify(response.data.user));
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } else {
      errorMessage.value = response.message || '保存失败';
    }
  } catch (error) {
    console.error('保存用户资料失败:', error);
    errorMessage.value = error.message || '保存失败，请检查网络连接';
  } finally {
    saving.value = false;
  }
};

const goToAddressManagement = (type) => {
  router.push(`/profile/addresses?type=${type}`);
};

const selectAvatar = () => {
  avatarInput.value?.click();
};

const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    errorMessage.value = '请选择图片文件';
    return;
  }
  
  // 验证文件大小（最大2MB）
  if (file.size > 2 * 1024 * 1024) {
    errorMessage.value = '图片大小不能超过2MB';
    return;
  }
  
  try {
    const formData = new FormData();
    formData.append('avatar', file);
    
    const response = await uploadAvatar(formData);
    
    if (response.code === 200) {
      profileForm.value.avatar = response.data.avatar_url;
      successMessage.value = '头像上传成功';
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } else {
      errorMessage.value = response.message || '头像上传失败';
    }
  } catch (error) {
    console.error('头像上传失败:', error);
    errorMessage.value = error.message || '头像上传失败，请检查网络连接';
  }
};

const handleAvatarError = (event) => {
  // 使用内联的默认头像数据URI，避免404错误
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjRjBGMEYwIi8+CjxjaXJjbGUgY3g9IjUwIiBjeT0iMzUiIHI9IjE1IiBmaWxsPSIjQzBDMEMwIi8+CjxwYXRoIGQ9Ik0yMCA3NUMzMCA2MCA0MCA2MCA1MCA2MEM2MCA2MCA3MCA2MCA4MCA3NUg4MFY4MEgyMFY3NVoiIGZpbGw9IiNDMEMwQzAiLz4KPC9zdmc+';
};

const showChangePasswordModal = () => {
  changePasswordVisible.value = true;
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
  passwordError.value = '';
};

const closeChangePasswordModal = () => {
  changePasswordVisible.value = false;
};

const changePassword = async () => {
  if (changingPassword.value) return;
  
  passwordError.value = '';
  
  // 验证表单
  if (!passwordForm.value.oldPassword) {
    passwordError.value = '请输入当前密码';
    return;
  }
  
  if (!passwordForm.value.newPassword || passwordForm.value.newPassword.length < 6) {
    passwordError.value = '新密码长度不能少于6位';
    return;
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordError.value = '两次输入的新密码不一致';
    return;
  }
  
  changingPassword.value = true;
  
  try {
    const response = await changePasswordAPI({
      old_password: passwordForm.value.oldPassword,
      new_password: passwordForm.value.newPassword
    });
    
    if (response.code === 200) {
      successMessage.value = '密码修改成功';
      closeChangePasswordModal();
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } else {
      passwordError.value = response.message || '密码修改失败';
    }
  } catch (error) {
    console.error('密码修改失败:', error);
    passwordError.value = error.message || '密码修改失败，请检查网络连接';
  } finally {
    changingPassword.value = false;
  }
};
</script>

<style scoped>
.profile-personal {
  background-color: #f5f5f7;
  min-height: 100vh;
  padding-bottom: 70px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.back-icon {
  font-size: 18px;
  cursor: pointer;
  color: #333;
}

.title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.save-btn {
  font-size: 16px;
  color: #4a90e2;
  cursor: pointer;
  font-weight: 500;
}

.save-btn.disabled {
  color: #999;
  cursor: not-allowed;
}

.avatar-section {
  display: flex;
  justify-content: center;
  padding: 30px;
  background-color: #fff;
  margin-bottom: 10px;
}

.avatar-container {
  position: relative;
  cursor: pointer;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #4a90e2;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
}

.form-section {
  background-color: #fff;
  margin-bottom: 10px;
}

.form-group {
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.form-group:last-child {
  border-bottom: none;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-bottom: 1px solid #e0e0e0;
  outline: none;
  font-size: 16px;
  background: transparent;
}

.form-input:focus {
  border-bottom-color: #4a90e2;
}

.form-value.readonly {
  padding: 10px 0;
  color: #666;
  font-size: 16px;
}

.form-note {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #999;
}

.gender-options {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.gender-option {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.gender-option input[type="radio"] {
  margin-right: 6px;
}

.gender-text {
  font-size: 16px;
}

.address-section {
  background-color: #fff;
  margin-bottom: 10px;
}

.section-header {
  padding: 20px 20px 10px;
  border-bottom: 1px solid #f0f0f0;
}

.section-header h3 {
  margin: 0 0 5px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.section-note {
  font-size: 12px;
  color: #999;
}

.address-group {
  padding: 0;
}

.address-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.address-item:last-child {
  border-bottom: none;
}

.address-item:hover {
  background-color: #f8f8f8;
}

.address-content {
  flex: 1;
}

.address-label {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.address-label i {
  margin-right: 8px;
  color: #4a90e2;
  width: 16px;
}

.address-label span {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.address-text {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.action-section {
  background-color: #fff;
  margin-bottom: 10px;
}

.action-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.action-item:last-child {
  border-bottom: none;
}

.action-item:hover {
  background-color: #f8f8f8;
}

.action-text {
  font-size: 16px;
  color: #333;
}

.error-message {
  background-color: #fff;
  margin: 10px 20px;
  padding: 10px 15px;
  border-radius: 6px;
  color: #e74c3c;
  font-size: 14px;
  border: 1px solid #fecaca;
  background-color: #fdf2f2;
}

.success-message {
  background-color: #fff;
  margin: 10px 20px;
  padding: 10px 15px;
  border-radius: 6px;
  color: #27ae60;
  font-size: 14px;
  border: 1px solid #86efac;
  background-color: #f0f9f0;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #357abd;
}

.btn-primary:disabled {
  background-color: #a0c7e8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background-color: #e8e8e8;
}
</style>