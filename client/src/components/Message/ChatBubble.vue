<template>
  <div class="chat-bubble-wrapper" :class="{ 'sender': isSender, 'receiver': !isSender }">
    <div v-if="!isSender" class="avatar-container">
      <img v-if="riderAvatar" :src="riderAvatar" alt="Rider Avatar" class="bubble-avatar" />
      <div v-else-if="riderNameInitial" class="bubble-avatar-placeholder">
        {{ riderNameInitial }}
      </div>
    </div>
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
  isSender: {
    type: Boolean,
    required: true,
  },
  riderAvatar: { // Pass rider avatar for receiver messages
    type: String,
    default: ''
  },
  riderNameInitial: { // Pass rider name initial for placeholder
    type: String,
    default: ''
  }
});

const formattedTime = computed(() => {
  if (!props.message.timestamp) return '';
  const date = new Date(props.message.timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
});
</script>

<style scoped>
.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 12px; /* Increased margin */
  max-width: 85%; /* Slightly wider max width */
  align-items: flex-end; /* Align avatar with bottom of bubble */
}

.chat-bubble-wrapper.sender {
  justify-content: flex-end;
  margin-left: auto;
}

.chat-bubble-wrapper.receiver {
  justify-content: flex-start;
  margin-right: auto;
}

.avatar-container {
  margin-right: 8px;
  flex-shrink: 0; /* Prevent avatar from shrinking */
}

.bubble-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #ccc; /* Placeholder bg */
}
.bubble-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #007bff; /* Or a color derived from rider's name */
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.chat-bubble {
  padding: 8px 12px; /* Adjusted padding */
  border-radius: 18px; /* More rounded bubbles */
  position: relative;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1); /* Subtle shadow for depth */
  min-width: 60px; /* Minimum width for small messages */
}

.sender .chat-bubble {
  background-color: #dcf8c6; /* Lighter green for sender */
  color: #303030;
  border-bottom-right-radius: 4px; /* Tail effect */
}

.receiver .chat-bubble {
  background-color: #ffffff;
  color: #303030;
  border-bottom-left-radius: 4px; /* Tail effect */
}

.message-text {
  margin: 0 0 4px 0;
  word-wrap: break-word;
  white-space: pre-wrap;
  font-size: 0.95rem; /* Slightly larger text */
  line-height: 1.4;
}

.message-time {
  font-size: 0.7rem;
  color: #888; /* Slightly darker for better contrast on white */
  display: block;
  text-align: right;
  margin-top: 2px; /* Space above time */
}

.sender .message-time {
  color: #6aa050; /* Time color consistent with sender bubble */
}
</style>