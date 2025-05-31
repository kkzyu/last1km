<template>
  <div class="profile-personal-page">
    <div class="page-header-container">
      <span class="back-icon" @click="goBack">
        <i class="fas fa-angle-left"></i>
      </span>
      <h2 class="title">个人资料</h2>
      <span class="save-button" @click="promptSaveAll" v-if="hasChanges">保存</span>
      <span class="save-button placeholder" v-else></span> </div>

    <div class="profile-list-container" v-if="userStore.userProfile">
      <div class="profile-item" @click="editField('avatar', '头像')">
        <span class="item-label">头像</span>
        <div class="item-content">
          <img class="avatar" :src="editableAvatarUrl" :alt="userStore.displayName || '用户头像'" @error="onAvatarError" />
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <div class="profile-item">
        <span class="item-label">用户名</span>
        <div class="item-content">
          <span class="item-value">{{ userStore.userProfile.username || '未设置' }}</span>
          </div>
      </div>

      <div class="profile-item" @click="editField('gender', '性别', editableGender)">
        <span class="item-label">性别</span>
        <div class="item-content">
          <span class="item-value">{{ displayGender(editableGender) }}</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <div class="profile-item" @click="editField('phone', '手机号', editablePhone)">
        <span class="item-label">手机号</span>
        <div class="item-content">
          <span class="item-value">{{ editablePhone || '未设置' }}</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>
      
      <div class="profile-item" @click="editField('school_info', '学校信息', editableSchoolInfo)">
        <span class="item-label">学校信息</span>
        <div class="item-content">
          <span class="item-value">{{ editableSchoolInfo || '未设置' }}</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <div class="profile-item last-item" @click="editField('dormitory', '宿舍', editableDormitory)">
        <span class="item-label">地址</span>
        <div class="item-content">
          <span class="item-value">{{ editableDormitory || '未设置' }}</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>
    </div>
    <div v-else class="loading-or-empty-state">
      <a-spin v-if="isLoading" />
      <a-empty v-else description="无法加载用户资料" />
    </div>

    <div class="actions-container">
      <AccountActions 
        @requestAccountManagement="handleRequestAccountManagement" 
        @logout="handleLogout" 
      />
    </div>

    <a-modal
      v-model:open="editModalVisible"
      :title="`修改${currentEditFieldLabel}`"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      :confirm-loading="modalConfirmLoading"
      :width="modalWidth" 
      destroy-on-close
    >
      <a-input v-if="currentEditField === 'nickname'" v-model:value="editModalValue" placeholder="请输入昵称" />
      <a-select v-if="currentEditField === 'gender'" v-model:value="editModalValue" placeholder="请选择性别" style="width: 100%">
        <a-select-option value="male">男</a-select-option>
        <a-select-option value="female">女</a-select-option>
        <a-select-option value="other">其他</a-select-option>
        <a-select-option value="secret">保密</a-select-option>
      </a-select>
      <a-input v-if="currentEditField === 'phone'" v-model:value="editModalValue" placeholder="请输入手机号" />
      <a-input v-if="currentEditField === 'school_info'" v-model:value="editModalValue" placeholder="请输入学校信息" />
      <a-input v-if="currentEditField === 'dormitory'" v-model:value="editModalValue" placeholder="请输入地址信息" />
      <div v-if="currentEditField === 'avatar'">
        <div class="avatar-upload-container">
          <div class="current-avatar-section">
            <h4 class="section-title">头像</h4>
            <div class="avatar-preview-wrapper" @click="triggerAvatarUpload">
              <img 
                :src="editableAvatarUrl" 
                class="current-avatar-preview" 
                @error="onAvatarError"
                :alt="userStore.displayName || '用户头像'"
              />
              <div class="avatar-hover-overlay">
                <div class="upload-icon-container">
                  <i class="fas fa-camera"></i>
                </div>
                <p class="upload-hint-text">点击更换头像</p>
              </div>
            </div>
            
            <!-- 隐藏的文件输入 -->
            <input 
              ref="fileInputRef" 
              type="file" 
              accept="image/jpeg,image/jpg,image/png" 
              @change="handleFileSelect" 
              style="display: none;"
            />
            
            <!-- 预览选中的新头像 -->
            <div v-if="newAvatarFile" class="new-avatar-preview">
              <h4 class="section-title">新头像预览</h4>
              <div class="preview-container">
                <img :src="newAvatarPreviewUrl" class="preview-image" />
                <div class="preview-actions">
                  <a-button size="small" @click="cancelAvatarSelection" style="margin-right: 8px;">
                    取消
                  </a-button>
                  <a-button type="primary" size="small" @click="confirmAvatarUpload">
                    确认上传
                  </a-button>
                </div>
              </div>
            </div>
            
            <div class="upload-tips">
              <p class="simple-tip">*支持 JPG、PNG 格式，文件大小不超过 2MB</p>
            </div>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { Modal as AModal, message, Input as AInput, Select as ASelect, SelectOption as ASelectOption, Upload as AUpload, Button as AButton, Spin as ASpin, Empty as AEmpty } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';
import AccountActions from '@/components/Profile/AccountActions.vue'; // Added import

const router = useRouter();
const userStore = useUserStore();

const isLoading = ref(true);

// 移除了 editableNickname，因为用户名现在是只读的
// const editableNickname = ref(''); 
const editableGender = ref('');
const editablePhone = ref('');
const editableSchoolInfo = ref('');
const editableDormitory = ref('');
const editableAvatarUrl = computed(() => userStore.avatarUrl);
const newAvatarFile = ref(null);
const avatarFileList = ref([]);
const fileInputRef = ref(null);
const newAvatarPreviewUrl = ref('');

const initialProfileData = ref({});
const hasChanges = computed(() => {
    if (!userStore.userProfile || !initialProfileData.value || Object.keys(initialProfileData.value).length === 0) return false;
    // 用户名 (username) 和 ID 不可编辑，所以不在此处比较
    // 昵称 (nickname) 如果仍然是可编辑字段 (虽然当前需求是改成显示username)，则需要比较
    // 如果您有一个独立的 nickname 字段仍然需要编辑，可以保留对它的比较
    // const nicknameChanged = userStore.userProfile.nickname !== initialProfileData.value.nickname; 
    return (
           (editableGender.value !== (initialProfileData.value.gender || '')) || // 添加空值保护
           (editablePhone.value !== (initialProfileData.value.phone || '')) ||
           (editableSchoolInfo.value !== (initialProfileData.value.school_info || '')) ||
           (editableDormitory.value !== (initialProfileData.value.dormitory || '')) ||
           newAvatarFile.value !== null
           // (nicknameChanged && editableFields.nickname) // 如果昵称仍可编辑
    );
});

watch(
  () => userStore.userProfile,
  (newProfile) => {
    if (newProfile) {
      // editableNickname.value = newProfile.nickname || ''; // 不再需要，username 直接从 store 读取
      editableGender.value = newProfile.gender || '';
      editablePhone.value = newProfile.phone || '';
      editableSchoolInfo.value = newProfile.school_info || '';
      editableDormitory.value = newProfile.dormitory || '';
      initialProfileData.value = { ...newProfile }; // 记录所有初始值
      newAvatarFile.value = null; 
      avatarFileList.value = [];
    }
    isLoading.value = false;
  },
  { immediate: true, deep: true }
);

onMounted(async () => {
  if (!userStore.userProfile) {
    isLoading.value = true;
    await userStore.fetchUserProfile();
  } else {
    // 如果 store 中已有数据，确保 initialProfileData 也被正确设置
    if (Object.keys(initialProfileData.value).length === 0 && userStore.userProfile) {
        // editableNickname.value = userStore.userProfile.nickname || '';
        editableGender.value = userStore.userProfile.gender || '';
        editablePhone.value = userStore.userProfile.phone || '';
        editableSchoolInfo.value = userStore.userProfile.school_info || '';
        editableDormitory.value = userStore.userProfile.dormitory || '';
        initialProfileData.value = { ...userStore.userProfile };
    }
    isLoading.value = false;
  }
});

const goBack = () => {
  if (hasChanges.value) {
    AModal.confirm({
      title: '提示',
      content: '您有未保存的更改，确定要离开吗？',
      okText: '确定离开',
      cancelText: '取消',
      onOk: () => {
        router.push('/profile');
      },
    });
  } else {
    router.push('/profile');
  }
};

const editModalVisible = ref(false);
const currentEditField = ref('');
const currentEditFieldLabel = ref('');
const editModalValue = ref('');
const modalConfirmLoading = ref(false);

const editField = (fieldKey, label, currentValue) => {
  if (fieldKey === 'username' || fieldKey === 'id') { 
    message.info('用户名/ID 不可修改。');
    return;
  }
  currentEditField.value = fieldKey;
  currentEditFieldLabel.value = label || ''; // 确保 label 有值
  if (fieldKey === 'avatar') {
    newAvatarFile.value = null; 
    avatarFileList.value = []; // 重置上传组件状态
  } else {
    editModalValue.value = currentValue === undefined || currentValue === null ? '' : String(currentValue);
  }
  editModalVisible.value = true;
};

const triggerAvatarUpload = () => {
  fileInputRef.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 验证文件类型
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('只能上传 JPG/PNG 格式的图片！');
    return;
  }
  
  // 验证文件大小
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('图片大小必须小于 2MB！');
    return;
  }
  
  // 存储文件并创建预览URL
  newAvatarFile.value = file;
  newAvatarPreviewUrl.value = URL.createObjectURL(file);
  
  // 清空文件输入的值，这样可以重复选择同一个文件
  event.target.value = '';
};

const cancelAvatarSelection = () => {
  if (newAvatarPreviewUrl.value) {
    URL.revokeObjectURL(newAvatarPreviewUrl.value);
  }
  newAvatarFile.value = null;
  newAvatarPreviewUrl.value = '';
};

const confirmAvatarUpload = async () => {
  if (!newAvatarFile.value) return;
  
  modalConfirmLoading.value = true;
  const success = await userStore.uploadUserAvatar(newAvatarFile.value);
  
  if (success) {
    cancelAvatarSelection(); // 清理预览
    editModalVisible.value = false;
  }
  
  modalConfirmLoading.value = false;
};

const handleModalOk = async () => {
  if (currentEditField.value === 'avatar') {
    if (newAvatarFile.value) {
      await confirmAvatarUpload();
    } else {
      editModalVisible.value = false;
    }
    return;
  }
  
  // 其他字段的处理逻辑保持不变
  modalConfirmLoading.value = true;
  let success = false;
  const fieldToUpdate = currentEditField.value;
  
  if (fieldToUpdate === 'phone' && editModalValue.value && !/^\d{7,15}$/.test(editModalValue.value)) {
    message.error('请输入有效的手机号');
    modalConfirmLoading.value = false;
    return;
  }
  
  const dataToUpdate = { [fieldToUpdate]: editModalValue.value };
  success = await userStore.updateUserProfile(dataToUpdate);
  
  if (success) {
    editModalVisible.value = false;
  }
  modalConfirmLoading.value = false;
};

const handleModalCancel = () => {
  if (currentEditField.value === 'avatar') {
    cancelAvatarSelection();
  }
  editModalVisible.value = false;
};

// 清理组件卸载时的预览URL
onBeforeUnmount(() => {
  if (newAvatarPreviewUrl.value) {
    URL.revokeObjectURL(newAvatarPreviewUrl.value);
  }
});

const displayGender = (genderValue) => {
  if (genderValue === 'male') return '男';
  if (genderValue === 'female') return '女';
  if (genderValue === 'other') return '其他';
  if (genderValue === 'secret') return '保密';
  return genderValue || '未设置';
};

const beforeAvatarUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('你只能上传 JPG/PNG 格式的图片!');
  }
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('图片大小必须小于 2MB!');
  }
  if (isJpgOrPng && isLt2M) {
    newAvatarFile.value = file; // 存储原始 File 对象
    // 更新 antd upload 组件的 fileList 以进行预览
    avatarFileList.value = [{
      uid: file.uid || Date.now().toString(), // 确保 uid 存在且唯一
      name: file.name,
      status: 'done', // 'done' 状态通常用于已上传或本地预览
      url: URL.createObjectURL(file) // 创建本地对象 URL 用于预览
    }];
  } else {
    // 验证失败，清空选择
    newAvatarFile.value = null;
    avatarFileList.value = [];
  }
  return false; // 阻止 antd upload 的默认上传行为
};

const handleAvatarUploadChange = (info) => {
  // 主要处理文件移除的情况，因为 beforeAvatarUpload 已经处理了文件选择
  if (info.file.status === 'removed') {
    newAvatarFile.value = null;
    avatarFileList.value = [];
  }
  // 如果 antd 的 fileList 与我们的状态不一致（例如，由于 maxCount），
  // 确保我们的 avatarFileList 是权威的。
  // 但由于 beforeUpload 返回 false 且 maxCount=1，通常不会出现不一致。
  // 如果 avatarFileList.value 与 info.fileList 不同步，可以强制同步：
  // if (info.fileList.length === 0 && newAvatarFile.value) {
  //   // 例如，如果用户清除了上传列表但我们仍有 newAvatarFile
  //   // (这种情况不常见，因为移除操作会触发 status === 'removed')
  // } else if (info.fileList.length > 0 && !newAvatarFile.value) {
  //   // 如果 antd 列表有文件但我们没有 newAvatarFile (例如，校验失败后 antd 仍保留)
  //   avatarFileList.value = [];
  // }
};

const promptSaveAll = async () => {
  if (!hasChanges.value) {
    message.info('没有检测到更改。');
    return;
  }
  
  const dataToUpdate = {};
  const originalProfile = initialProfileData.value;

  if (editableGender.value !== (originalProfile.gender || '')) dataToUpdate.gender = editableGender.value;
  if (editablePhone.value !== (originalProfile.phone || '')) dataToUpdate.phone = editablePhone.value;
  if (editableSchoolInfo.value !== (originalProfile.school_info || '')) dataToUpdate.school_info = editableSchoolInfo.value;
  if (editableDormitory.value !== (originalProfile.dormitory || '')) dataToUpdate.dormitory = editableDormitory.value;

  let avatarUpdateProcessed = false; // 标记是否处理了头像

  if (newAvatarFile.value) {
    avatarUpdateProcessed = true;
    message.loading({ content: '正在上传头像...', key: 'avatarUploadSaveAll' });
    const avatarSuccess = await userStore.uploadUserAvatar(newAvatarFile.value);
    if (avatarSuccess) {
      message.success({ content: '头像上传成功!', key: 'avatarUploadSaveAll', duration: 2 });
      newAvatarFile.value = null;
      avatarFileList.value = [];
    } else {
      message.error({ content: '头像上传失败，请重试。其他更改未保存。', key: 'avatarUploadSaveAll', duration: 3 });
      return; // 如果头像上传失败，则不继续保存其他信息
    }
  }

  if (Object.keys(dataToUpdate).length > 0) {
    AModal.confirm({
      title: '保存更改',
      content: '您确定要保存对个人资料的修改吗？',
      okText: '保存',
      cancelText: '取消',
      onOk: async () => {
        const textUpdateSuccess = await userStore.updateUserProfile(dataToUpdate);
        if (textUpdateSuccess) {
          // initialProfileData 会通过 watch 更新
          // newAvatarFile 应该在头像上传成功后已清空
        }
      },
    });
  } else if (avatarUpdateProcessed) {
    // 仅头像被更改并成功上传
    // message.success('个人资料已更新！'); // 头像上传成功消息已由 uploadUserAvatar 显示
  } else {
     // 此情况理论上不应发生，因为 hasChanges.value 为 true
    message.info('没有需要保存的更改。');
  }
};

const APP_PUBLIC_BASE_URL = (typeof import.meta.env !== 'undefined' && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/';
const fallbackAvatar = `${APP_PUBLIC_BASE_URL}images/ProfilePortrait.jpg`;
const onAvatarError = (event) => {
  event.target.src = fallbackAvatar;
};

const modalWidth = computed(() => {
  if (currentEditField.value === 'avatar') {
    // 如果是编辑头像，上传界面可能内容较多，可以给一个稍宽的宽度
    return '300px'; 
  }
  // 其他如昵称、性别、手机号等简单输入项，使用较窄的宽度
  return '260px'; 
});

// Added event handlers for AccountActions component
const handleRequestAccountManagement = () => {
  router.push('/profile/account-management');
};

const handleLogout = () => {
  AModal.confirm({
    title: '退出登录',
    content: '您确定要退出当前账号吗？',
    okText: '确定退出',
    cancelText: '取消',
    centered: true,
    onOk: () => {
      userStore.clearUserProfile();
      message.success('您已成功退出登录！');
      router.push('/login');
    },
  });
};

watch(
  () => userStore.userProfile,
  (newProfile) => {
    if (newProfile) {
      editableGender.value = newProfile.gender || '';
      editablePhone.value = newProfile.phone || '';
      editableSchoolInfo.value = newProfile.school_info || '';
      editableDormitory.value = newProfile.dormitory || '';
      initialProfileData.value = { ...newProfile };
      newAvatarFile.value = null;
      avatarFileList.value = [];
    }
    isLoading.value = false;
  },
  { immediate: true, deep: true }
);

onMounted(async () => {
  if (!userStore.userProfile) {
    isLoading.value = true;
    await userStore.fetchUserProfile();
  } else {
    if (Object.keys(initialProfileData.value).length === 0 && userStore.userProfile) {
        editableGender.value = userStore.userProfile.gender || '';
        editablePhone.value = userStore.userProfile.phone || '';
        editableSchoolInfo.value = userStore.userProfile.school_info || '';
        editableDormitory.value = userStore.userProfile.dormitory || '';
        initialProfileData.value = { ...userStore.userProfile };
    }
    isLoading.value = false;
  }
});

</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.profile-personal-page {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 占据整个视口高度 */
  background-color: #f8f9fa;
  padding-bottom: 80px; /* 为底部的按钮区域留出空间 */
}
.page-header-container {
  display: flex;
  padding: 12px 16px; /* 调整内边距 */
  align-items: center;
  background-color: #ffffff; /* 白色背景 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* 微小阴影 */
  position: sticky; /* 使头部固定 */
  top: 0;
  z-index: 100; /* 确保在最上层 */
  height: 50px; /* 固定头部高度 */
  box-sizing: border-box;
}
.back-icon {
  font-size: 20px; /* 调整图标大小 */
  color: #333;
  cursor: pointer;
  transition: color 0.2s;
  padding: 8px; /* 增加点击区域 */
  margin-left: -8px; /* 抵消padding */
}
.back-icon:hover {
  color: #1890ff;
}
.title {
  flex: 1;
  text-align: center;
  margin: 0;
  font-size: 17px; /* 调整标题字体大小 */
  font-weight: 600;
  color: #333;
}
.save-button {
  font-size: 15px;
  color: #1890ff;
  cursor: pointer;
  padding: 8px;
  min-width: 50px; /* 给保存按钮一个最小宽度以便对齐 */
  text-align: right;
}
.save-button.placeholder {
    visibility: hidden; /* 占位但不显示 */
}

.profile-list-container {
  padding: 0 16px;
  flex-grow: 1; /* 使列表区域可滚动 */
  overflow-y: auto;
  padding-top: 10px; /* 列表与头部的间距 */
}
.profile-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0; /* 更浅的分割线 */
  cursor: pointer; /* 使整个条目可点击 */
  background-color: #fff; /* 列表项背景 */
  padding-left: 12px; /* 统一内边距 */
  padding-right: 12px;
}
.profile-item:first-child {
    border-top-left-radius: 8px; /* 圆角 */
    border-top-right-radius: 8px;
}
.profile-item.last-item {
  border-bottom: none; /* 最后一项无下边框 */
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  margin-bottom: 20px; /* 列表底部留白 */
}
.item-label {
  font-size: 15px; /* 调整字体大小 */
  color: #333;
}
.item-content {
  display: flex;
  align-items: center;
  gap: 8px;
}
.item-value {
  font-size: 15px; /* 调整字体大小 */
  color: #888; /* 值颜色变浅 */
}
.avatar {
  width: 48px; /* 增大头像尺寸 */
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #f0f0f0;
}
.arrow-icon {
  color: #ccc; /* 箭头颜色变浅 */
  font-size: 14px;
}
.loading-or-empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 50px); /* 减去头部高度 */
}

/* 头像上传容器样式 */
.avatar-upload-container {
  padding: 8px 0;
  max-width: 100%;
}

.current-avatar-section {
  text-align: center;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #262626;
  margin: 0 0 20px 0;
  text-align: center;
}

.avatar-preview-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
  margin-bottom: 20px;
}

.current-avatar-preview {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f0f0;
  transition: all 0.3s ease;
  display: block;
}

.avatar-hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
}

.avatar-preview-wrapper:hover .avatar-hover-overlay {
  opacity: 1;
}

.avatar-preview-wrapper:hover .current-avatar-preview {
  transform: scale(1.02);
}

.upload-icon-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.upload-icon-container i {
  font-size: 18px;
  color: white;
}

.upload-hint-text {
  font-size: 12px;
  color: white;
  margin: 0;
  font-weight: 500;
}

/* 新头像预览区域 */
.new-avatar-preview {
  margin-top: 14px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.preview-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #1890ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
}

.preview-actions {
  display: flex;
  gap: 8px;
}

/* 提示信息样式 */
.upload-tips {
  margin-top: 5px;
  text-align: left;
}

.simple-tip {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

/* 模态框样式优化 */
:deep(.ant-modal-content) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.ant-modal-header) {
  background: linear-gradient(135deg, #fafbfc 0%, #f4f6f8 100%);
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 24px;
}

:deep(.ant-modal-title) {
  font-weight: 600;
  color: #262626;
}

:deep(.ant-modal-body) {
  padding: 24px;
  min-height: 200px;
}

:deep(.ant-modal-footer) {
  border-top: 1px solid #f0f0f0;
  padding: 12px 24px;
}

/* AccountActions component styles */
.account-actions-container {
  margin-top: 24px;
  padding: 0 16px; /* Match horizontal padding of other elements like profile-list-container */
  margin-bottom: 20px; /* Provide some space at the bottom */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .avatar-upload-container {
    padding: 0;
  }
  
  .current-avatar-preview {
    width: 80px;
    height: 80px;
  }
  
  .preview-image {
    width: 60px;
    height: 60px;
  }
  
  .upload-icon-container {
    width: 32px;
    height: 32px;
  }
  
  .upload-icon-container i {
    font-size: 14px;
  }
  
  .upload-hint-text {
    font-size: 11px;
  }
}

.actions-container {
  /* Styles for the container of AccountActions if needed, 
     can be placed fixed at bottom or as part of scrollable content */
  /* For example, to make it part of the scrollable content: */
  margin-top: 20px; /* Adjust as needed */
  padding: 0 16px; /* Match AccountActions.vue padding if desired */
}
</style>