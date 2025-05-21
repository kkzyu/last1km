<template>
  <li class="message-list-item">
    <img :src="fullAvatarUrl" :alt="chat.rider.name" class="avatar" @click.stop="navigateToRiderProfile(chat.rider.id)"/>
    <div class="message-content">
      <div class="info-header">
        <span class="rider-name">{{ chat.rider.name }}</span>
        <span class="timestamp">{{ formattedTimestamp }}</span>
      </div>
      <p class="last-message">{{ chat.lastMessage }}</p>
    </div>
    <div v-if="chat.unreadCount > 0" class="unread-badge">{{ chat.unreadCount }}</div>
  </li>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  chat: {
    type: Object,
    required: true,
  },
});

const router = useRouter();
const BASE_URL = import.meta.env.BASE_URL;

const fullAvatarUrl = computed(() => {
  const avatarPath = props.chat.rider.avatar; // 例如 "/images/avatar1.jpg"

  // 如果 avatarPath 为空或不是字符串，返回一个占位符或空字符串
  if (!avatarPath || typeof avatarPath !== 'string') {
    return ''; // 或者一个默认的占位符图片路径
  }

  // 如果 BASE_URL 是根路径 ('/'), 那么 avatarPath 已经是正确的
  if (BASE_URL === '/') {
    return avatarPath;
  }

  // 否则，我们需要将 BASE_URL 和 avatarPath 拼接起来
  // 确保 BASE_URL 没有尾部斜杠，因为 avatarPath 已经以斜杠开头
  const cleanBase = BASE_URL.endsWith('/') ? BASE_URL.slice(0, -1) : BASE_URL;

  // 拼接：例如 "/last1km" + "/images/avatar1.jpg" = "/last1km/images/avatar1.jpg"
  return `${cleanBase}${avatarPath}`;
});

const formattedTimestamp = computed(() => {
  const date = new Date(props.chat.timestamp);
  // 简单的时间格式化，你可以用更完善的库如 date-fns
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  return date.toLocaleDateString();
});

const navigateToRiderProfile = (riderId) => {
  router.push({ name: 'rider-profile', params: { riderId } });
};
</script>

<style scoped>
.message-list-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}
.message-list-item:hover {
  background-color: #f9f9f9;
}
.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 0.75rem;
  object-fit: cover;
  cursor: pointer; /* 使头像可点击跳转到骑手主页 */
}
.message-content {
  flex-grow: 1;
  overflow: hidden; /* 防止长文本溢出 */
}
.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}
.rider-name {
  font-weight: bold;
}
.timestamp {
  font-size: 0.8rem;
  color: #666;
}
.last-message {
  font-size: 0.9rem;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}
.unread-badge {
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 0.1em 0.4em;
  font-size: 0.8rem;
  /* min-width: 1.0em; 保证圆形 */
  height: 1.2em;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 0.5rem;
}
</style>