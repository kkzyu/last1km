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
      <div class="profile-item" @click="editField('avatar')">
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

    <a-modal
      v-model:open="editModalVisible"
      :title="`修改${currentEditFieldLabel}`"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      :confirm-loading="modalConfirmLoading"
      :width="modalWidth"
    >
      <a-select v-if="currentEditField === 'gender'" v-model:value="editModalValue" placeholder="请选择性别" style="width: 100%">
        <a-select-option value="male">男</a-select-option>
        <a-select-option value="female">女</a-select-option>
        <a-select-option value="other">其他</a-select-option>
        <a-select-option value="secret">保密</a-select-option>
      </a-select>
      <a-input v-if="currentEditField === 'phone'" v-model:value="editModalValue" placeholder="请输入手机号" />
      <a-input v-if="currentEditField === 'school_info'" v-model:value="editModalValue" placeholder="请输入学校信息" />
      <a-input v-if="currentEditField === 'dormitory'" v-model:value="editModalValue" placeholder="请输入宿舍信息" />
      <div v-if="currentEditField === 'avatar'">
        <p>当前头像:</p>
        <img :src="editableAvatarUrl" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px;" @error="onAvatarError"/>
        <a-upload
          name="avatarFile"
          list-type="picture"
          :max-count="1"
          :before-upload="beforeAvatarUpload"
          @change="handleAvatarUploadChange"
          :file-list="avatarFileList"
        >
          <a-button>
            <UploadOutlined /> 点击上传新头像
          </a-button>
        </a-upload>
        <span style="font-size: 12px; color: #999;">*仅支持JPG/PNG, 小于2MB</span>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { Modal as AModal, message, Input as AInput, Select as ASelect, SelectOption as ASelectOption, Upload as AUpload, Button as AButton, Spin as ASpin, Empty as AEmpty } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';

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
  // 用户名 (username) 和 ID 通常不允许编辑
  if (fieldKey === 'username' || fieldKey === 'id') { 
    message.info('用户名/ID 不可修改。');
    return;
  }
  currentEditField.value = fieldKey;
  currentEditFieldLabel.value = label;
  if (fieldKey === 'avatar') {
    newAvatarFile.value = null; 
    avatarFileList.value = [];
  } else {
    editModalValue.value = currentValue || '';
  }
  editModalVisible.value = true;
};

const handleModalOk = async () => {
  modalConfirmLoading.value = true;
  let success = false;
  const fieldToUpdate = currentEditField.value;

  if (fieldToUpdate === 'avatar') {
    if (newAvatarFile.value) {
      // ... (头像上传逻辑，如前所述)
      // 假设上传成功，后端返回了新的头像文件名 'new_avatar_filename.jpg'
      // success = await userStore.updateUserProfile({ avatar: 'new_avatar_filename.jpg' });
      message.info('头像上传功能待实现。若已实现，请在此处调用真实上传并更新 store。');
      success = true; // 仅为示例流程，假设模拟成功
      if (success) {
          newAvatarFile.value = null;
          avatarFileList.value = [];
          // 通常 updateUserProfile 成功后，store 的 userProfile 会更新，
          // watch 会自动更新 initialProfileData.value
          // 但如果只是模拟，需要手动更新 initialProfileData 的 avatar 部分（如果适用）
          if (userStore.userProfile) initialProfileData.value.avatar = userStore.userProfile.avatar;
      }
    } else {
      message.info('没有选择新的头像文件。');
      modalConfirmLoading.value = false;
      editModalVisible.value = false;
      return;
    }
  } else {
    if (fieldToUpdate === 'phone' && editModalValue.value && !/^\d{7,15}$/.test(editModalValue.value)) { // 更通用的手机号校验
      message.error('请输入有效的手机号');
      modalConfirmLoading.value = false;
      return;
    }
    // 昵称 (nickname) 字段已经移除，所以这里不需要处理 nickname 的空值校验
    // if (typeof editModalValue.value === 'string' && editModalValue.value.trim() === '' && (fieldToUpdate === 'nickname')) {
    //     message.error(`${currentEditFieldLabel.value}不能为空`);
    //     modalConfirmLoading.value = false;
    //     return;
    // }

    const dataToUpdate = { [fieldToUpdate]: editModalValue.value };
    success = await userStore.updateUserProfile(dataToUpdate);
  }
  
  if (success) {
    editModalVisible.value = false;
    // 如果 updateUserProfile 成功，watch 会更新 initialProfileData
  }
  modalConfirmLoading.value = false;
};

const handleModalCancel = () => {
  editModalVisible.value = false;
  newAvatarFile.value = null;
  avatarFileList.value = [];
};

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
    newAvatarFile.value = file; 
    avatarFileList.value = [{ uid: file.uid || '-1', name: file.name, status: 'done', url: URL.createObjectURL(file) }]; // 本地预览
  } else {
    avatarFileList.value = []; // 清除非法文件
    newAvatarFile.value = null;
  }
  return false; 
};

const handleAvatarUploadChange = (info) => {
  if (info.file.status === 'removed') {
    newAvatarFile.value = null;
    avatarFileList.value = [];
  } else if (info.fileList.length > 0) {
      // beforeAvatarUpload 已经处理了 newAvatarFile 和 fileList 的更新
      // 这里主要是为了响应 antd upload 组件自身的状态变化，确保 fileList 同步
      // 如果 beforeAvatarUpload 校验失败，antd 内部可能还是会尝试更新它的 fileList
      // 所以确保我们的 fileList 与 newAvatarFile (代表我们认可的文件) 一致
      if (newAvatarFile.value) {
          // 确保显示的是我们已校验并存储的文件
          const validFileEntry = avatarFileList.value.find(f => f.originFileObj === newAvatarFile.value || f === newAvatarFile.value);
          if (validFileEntry) {
              avatarFileList.value = [validFileEntry];
          } else { // 如果 antd 添加了一个我们不认可的文件
              avatarFileList.value = [];
              newAvatarFile.value = null;
          }
      } else { // 如果 newAvatarFile 为空，说明校验失败或已移除
          avatarFileList.value = [];
      }

  } else { // info.fileList 为空
      newAvatarFile.value = null;
      avatarFileList.value = [];
  }
};

const promptSaveAll = async () => {
  if (!hasChanges.value) {
    message.info('没有检测到更改。');
    return;
  }
  // 创建一个只包含已更改字段的对象
  const dataToUpdate = {};
  const originalProfile = initialProfileData.value;
  const currentProfile = userStore.userProfile; // 获取最新的 store 数据作为比较基准

  // 比较并收集非用户名/ID 的更改
  if (editableGender.value !== (originalProfile.gender || '')) dataToUpdate.gender = editableGender.value;
  if (editablePhone.value !== (originalProfile.phone || '')) dataToUpdate.phone = editablePhone.value;
  if (editableSchoolInfo.value !== (originalProfile.school_info || '')) dataToUpdate.school_info = editableSchoolInfo.value;
  if (editableDormitory.value !== (originalProfile.dormitory || '')) dataToUpdate.dormitory = editableDormitory.value;
  // 如果您仍然有一个独立的、可编辑的昵称字段，在这里添加比较
  // if (currentProfile.nickname !== originalProfile.nickname) dataToUpdate.nickname = currentProfile.nickname;


  // **头像上传逻辑** (重要: 这部分需要您实现实际的API调用)
  let avatarUpdateSuccess = true; // 标记头像更新是否成功 (如果尝试了的话)
  if (newAvatarFile.value) {
    message.loading({ content: '正在上传头像...', key: 'avatarUpload' });
    // 示例： const success = await userStore.uploadUserAvatarAction(newAvatarFile.value);
    // 上传成功后，userStore.uploadUserAvatarAction 应该会更新 userProfile.avatar
    // 并且后端 updateProfile 接口可能不再需要单独处理 avatar 字段，或者仍然需要传递新的 avatar 文件名
    // 假设上传成功，并且 userStore.userProfile.avatar 已经被更新为新的文件名/路径
    // dataToUpdate.avatar = userStore.userProfile.avatar; // 将新的头像名加入待更新列表
    // newAvatarFile.value = null; // 清空
    // avatarFileList.value = [];
    // message.success({ content: '头像上传成功!', key: 'avatarUpload', duration: 2 });
    // avatarUpdateSuccess = success;
    message.warn({ content: '头像上传功能待实现。若要保存头像更改，请在此处集成真实上传逻辑。', key: 'avatarUpload', duration: 3 });
    // 为演示，暂时不将头像加入 dataToUpdate，除非您已实现上传并获取到新文件名
    // 如果您实现了上传并获得新文件名 newAvatarFilename，则: dataToUpdate.avatar = newAvatarFilename;
  }

  if (!avatarUpdateSuccess) { // 如果头像上传失败，则不继续保存其他信息
      message.error('头像更新失败，请重试。');
      return;
  }

  if (Object.keys(dataToUpdate).length > 0) {
    AModal.confirm({
      title: '保存更改',
      content: '您确定要保存对个人资料的修改吗？',
      okText: '保存',
      cancelText: '取消',
      onOk: async () => {
        const success = await userStore.updateUserProfile(dataToUpdate);
        if (success) {
          initialProfileData.value = { ...userStore.userProfile }; // 更新初始数据以重置 hasChanges
          newAvatarFile.value = null; // 确保在成功保存后清除，避免重复标记为更改
          avatarFileList.value = [];
        }
      },
    });
  } else if (newAvatarFile.value && Object.keys(dataToUpdate).length === 0) {
    // 这种情况是：只改了头像，但头像上传逻辑还没把 avatar 字段加入 dataToUpdate
    message.info('头像已选择，请点击“保存”以完成头像更新（需实现上传逻辑）。');
  } else {
    message.info('没有需要保存的文本信息更改。');
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

</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.profile-personal-page {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 占据整个视口高度 */
  background-color: #f8f9fa;
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


</style>