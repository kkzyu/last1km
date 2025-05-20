<template>
  <div class="chat-bubble-wrapper" :class="{ 'sender': isSender, 'receiver': !isSender }">
    <div class="chat-bubble">
      <p class="message-text">{{ message.text }}</p>
      <span class="message-time">{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isSender: { // true 表示是当前用户发送的，false 表示是对方（骑手）发送的
    type: Boolean,
    required: true,
  },
});

const formattedTime = computed(() => {
  const date = new Date(props.message.timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
});
</script>

<style scoped>
.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 0.75rem;
  max-width: 80%; /* 气泡最大宽度 */
}
.chat-bubble-wrapper.sender {
  justify-content: flex-end; /* 发送者消息靠右 */
  margin-left: auto; /* 确保靠右 */
}
.chat-bubble-wrapper.receiver {
  justify-content: flex-start; /* 接收者消息靠左 */
  margin-right: auto; /* 确保靠左 */
}
.chat-bubble {
  padding: 0.6rem 0.9rem;
  border-radius: 12px;
  position: relative;
}
.sender .chat-bubble {
  background-color: #95ec69; /* 发送者气泡颜色 (类似微信) */
  color: #000;
  border-top-right-radius: 0; /* 小三角效果 */
}
.receiver .chat-bubble {
  background-color: #ffffff; /* 接收者气泡颜色 */
  color: #000;
  border-top-left-radius: 0; /* 小三角效果 */
}
.message-text {
  margin: 0 0 0.25rem 0;
  word-wrap: break-word; /* 长单词换行 */
  white-space: pre-wrap; /* 保留换行符 */
}
.message-time {
  font-size: 0.7rem;
  color: #888;
  display: block;
  text-align: right; /* 时间戳通常在气泡内右下角 */
}
.sender .message-time {
  color: #777;
}
</style>