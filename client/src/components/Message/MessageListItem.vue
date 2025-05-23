<template>
  <a-list-item class="message-list-item" @click="handleClick">
    <a-list-item-meta>
      <template #avatar>
        <a-avatar :size="40" :src="fullAvatarUrl" @click.stop="navigateToRiderProfile(chat.rider.id)">
          {{ chat.rider.name ? chat.rider.name[0] : 'U' }} <!-- 头像占位符 -->
        </a-avatar>
      </template>
      <template #title>
        <div class="info-header">
          <span class="rider-name">{{ chat.rider.name }}</span>
          <span class="timestamp">{{ formattedTimestamp }}</span>
        </div>
      </template>
      <template #description>
        <div class="message-badge-line">
          <p class="last-message">{{ chat.lastMessage }}</p>
          <a-badge :count="chat.unreadCount" :overflow-count="99" class="custom-badge" v-if="chat.unreadCount > 0" />
        </div>
      </template>
    </a-list-item-meta>
  </a-list-item>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { ListItem as AListItem, ListItemMeta as AListItemMeta, Avatar as AAvatar, Badge as ABadge } from 'ant-design-vue';

const props = defineProps({
  chat: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['click']);

const router = useRouter();

// BASE_URL 处理逻辑保持不变，但需要确保 import.meta.env.BASE_URL 能正确获取
const BASE_URL = import.meta.env.BASE_URL || ''; // 提供一个默认值以防万一

const fullAvatarUrl = computed(() => {
  const avatarPath = props.chat.rider?.avatar; 

  if (!avatarPath || typeof avatarPath !== 'string') {
    return undefined; // Ant Design Avatar 组件在 src 为 undefined 时会显示子内容 (如文字)
  }
  // 假设 avatarPath 已经是完整的 URL 或者相对于服务器根目录的路径
  // 如果 avatarPath 是像 '/images/avatar1.jpg' 这样的相对路径，并且应用部署在子目录（如 /app/）
  // 则可能需要前缀 BASE_URL，例如 `${BASE_URL.replace(/\/$/, '')}${avatarPath}`
  // 这里的逻辑取决于您的项目部署和静态资源服务方式
  if (avatarPath.startsWith('http')) {
    return avatarPath; // 已经是完整 URL
  }
  // 修正 BASE_URL 和 avatarPath 的拼接逻辑
  const cleanBase = BASE_URL.endsWith('/') ? BASE_URL.slice(0, -1) : BASE_URL;
  const cleanAvatarPath = avatarPath.startsWith('/') ? avatarPath : `/${avatarPath}`;
  return `${cleanBase}${cleanAvatarPath}`; 
});

const formattedTimestamp = computed(() => {
  if (!props.chat.timestamp) return '';
  const date = new Date(props.chat.timestamp);
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
  }
  return date.toLocaleDateString();
});

const navigateToRiderProfile = (riderId) => {
  if (riderId) {
    router.push({ name: 'rider-profile', params: { riderId } });
  }
};

const handleClick = () => {
  emit('click');
};
</script>

<style scoped>
.message-list-item {
  /* a-list-item 已经有一些默认样式，我们在这里进行微调 */
  padding: 12px 0 !important; /* 覆盖 Ant 内联样式，使其与 MessagesHome 的 padding 匹配 */
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.message-list-item:hover {
  background-color: #f7f7f7; /* 悬停效果 */
}

.avatar {
  /* AAvatar 已经处理了样式，这里主要是确保点击区域 */
  cursor: pointer;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center; /* Center rider name and timestamp vertically */
  /* margin-bottom is removed as description now handles spacing if any */
}

.rider-name {
  font-weight: 500; /* Ant Design 风格的字重 */
  font-size: 14px;
  color: rgba(0, 0, 0, 0.85);
  /* Allow rider name to shrink if space is needed */
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 8px; /* Add some space between name and the timestamp/badge group */
  line-height: 1.4; /* Adjust line-height to better align with timestamp if needed */
}

.timestamp {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  white-space: nowrap;
  line-height: 1.4; /* Match rider-name or adjust as needed for visual balance */
  flex-shrink: 0; /* Prevent timestamp from shrinking */
}

/* Styles for the line containing last message and badge */
.message-badge-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px; /* Add some space below the title line */
}

.last-message {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
  /* Allow message to take available space but also shrink */
  flex-grow: 1;
  min-width: 0; 
  margin-right: 8px; /* Space between message and badge */
}

.custom-badge {
  margin-left: 0; 
  margin-top: 0; /* Reset margin-top as it's now inline with message */
  flex-shrink: 0; /* Prevent badge from shrinking */
}

:deep(.custom-badge .ant-badge-count) {
  background-color: #ff4d4f;
  box-shadow: 0 0 0 1px #fff;
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  font-size: 11px;
  padding: 0 4px;
}

/* 针对 a-list-item-meta 的内部元素进行样式调整 */
:deep(.ant-list-item-meta-content) {
  overflow: hidden; /* 确保 description 不会撑开布局 */
}

/* Removed :deep(.ant-list-item-action) as badge is no longer in actions slot */
</style>