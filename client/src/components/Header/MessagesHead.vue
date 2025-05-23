<template>
  <a-page-header class="messages-header" title="消息列表">
    <template #extra>
      <a-tooltip title="一键已读">
        <a-button 
          type="text" 
          shape="circle"
          @click="$emit('mark-all-read')" 
          :disabled="!hasUnreadMessages"
          aria-label="一键已读"
        >
          <template #icon><MailOutlined /></template>
        </a-button>
      </a-tooltip>
    </template>
  </a-page-header>
</template>

<script setup>
import { PageHeader as APageHeader, Button as AButton, Tooltip as ATooltip } from 'ant-design-vue';
import { MailOutlined } from '@ant-design/icons-vue'; // 使用 Ant Design Icon

defineProps({
  hasUnreadMessages: Boolean
})

// defineEmits 已被移除，因为 $emit 在模板中直接使用
</script>

<style scoped>
.messages-header {
  background-color: #fff; /* 更改为白色背景，更接近 Ant Design 风格 */
  border-bottom: 1px solid #f0f0f0; /* 添加底部边框 */
  padding: 12px 24px; /* Ant Design PageHeader 默认 padding，可以调整 */
}

/* 如果需要覆盖 PageHeader 内部组件的样式，可以使用 :deep() */
:deep(.ant-page-header-heading-title) {
  font-weight: 600; /* 调整标题字重 */
  font-size: 18px; /* 调整标题字体大小 */
}

/* 按钮样式调整，确保图标颜色和大小合适 */
.ant-btn.ant-btn-text {
  color: rgba(0, 0, 0, 0.65); /* 默认文本按钮颜色 */
  font-size: 18px; /* 图标大小 */
}

.ant-btn.ant-btn-text:hover,
.ant-btn.ant-btn-text:focus {
  color: #1890ff; /* Ant Design 主题色 */
  background-color: transparent;
}

.ant-btn[disabled] {
  color: rgba(0, 0, 0, 0.25) !important;
  cursor: not-allowed !important;
}
</style>