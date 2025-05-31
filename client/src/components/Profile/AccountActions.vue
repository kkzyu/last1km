<template>
  <div class="account-actions-wrapper">
    <button class="action-button switch" @click="onRequestAccountManagement">
      切换账号
    </button>
    <button class="action-button logout" @click="onLogout">
      退出登录
    </button>
  </div>
</template>

<script setup>
const emit = defineEmits(['requestAccountManagement', 'logout']);

const onRequestAccountManagement = () => {
  emit('requestAccountManagement');
};

const onLogout = () => {
  emit('logout');
};
</script>

<style scoped>
.account-actions-wrapper {
  margin-top: 40px; /* 增加与上方区块的间距 */
  padding: 0 16px; /* 调整内边距 */
  display: flex;
  flex-direction: column;
  gap: 16px; /* 增加按钮间距 */
}

.action-button {
  padding: 12px 20px; /* 调整内边距 */
  border-radius: 10px; /* 更大的圆角 */
  font-size: 0.95rem; /* 略微调整字体大小 */
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); /* 更平滑的过渡 */
  text-align: center;
  border: 1px solid transparent; /* 预留边框位置 */
  letter-spacing: 0.5px; /* 增加字间距 */
}

.action-button:active {
  transform: scale(0.97); /* 调整点击反馈 */
}

.switch {
  background-color: #f8f9fa; /* 非常浅的灰色背景 */
  color: #495057; /* 深灰色字体，更柔和 */
  border-color: #adb5bd; /* 调整为更深的灰色边框，例如 Bootstrap 的 $gray-500 */
}

.logout {
  background-color: transparent; /* 透明背景 */
  color: #e74c3c; /* 现代红色 */
  border: 1px solid #e74c3c; /* 红色边框 */
}

/* For hover effects */
@media (hover: hover) {
  .switch:hover {
    background-color: #e9ecef; /* 悬停时背景变深一点 */
    border-color: #9da6af; /* 悬停时边框也相应调整，可以比默认状态略深或保持一致 */
    transform: translateY(-1px); /* 轻微上移效果 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); /* 添加细微阴影 */
  }
  .logout:hover {
    background-color: rgba(231, 76, 60, 0.05); /* 悬停时非常浅的红色背景 */
    color: #c0392b; /* 悬停时字体颜色变深 */
    border-color: #c0392b; /* 悬停时边框颜色变深 */
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(231, 76, 60, 0.1);
  }
}
</style>
