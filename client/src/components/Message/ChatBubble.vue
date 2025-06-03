<template>
  <div class="chat-bubble-wrapper" :class="{ 'sender': isSender, 'receiver': !isSender }">
    <a-avatar v-if="!isSender" :size="36" :src="avatarSrc" class="bubble-avatar">
      {{ nameInitial }}
    </a-avatar>
    <div class="chat-bubble" :class="{ 'has-tail': true }">
      <div class="message-content">
        <p class="message-text">{{ message.text }}</p>
      </div>
      <span class="message-time">{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Avatar as AAvatar } from 'ant-design-vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isSender: {
    type: Boolean,
    required: true,
  },
  // For receiver, these will be rider's details
  avatarSrc: {
    type: String,
    default: ''
  },
  nameInitial: { // Fallback if avatarSrc is not available
    type: String,
    default: ''
  }
});

const formattedTime = computed(() => {
  if (!props.message.timestamp) return '';
  const date = new Date(props.message.timestamp);
  // Use a more modern time format, e.g., HH:mm
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
});
</script>

<style scoped>
/* Modern Chat Bubble Design */
:root {
  --primary-color: #007AFF;
  --sender-bg: linear-gradient(135deg, #007AFF 0%, #5856d6 100%);
  --sender-text-color: #FFFFFF;
  --receiver-bg: rgba(255, 255, 255, 0.9);
  --receiver-text-color: #1a1a1a;
  --text-color-secondary: rgba(26, 26, 26, 0.6);
  --bubble-border-radius: 20px;
  --avatar-size: 40px;
  --bubble-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  --bubble-shadow-hover: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 20px;
  max-width: 85%;
  align-items: flex-end;
  animation: fadeInUp 0.3s ease-out;
}

.chat-bubble-wrapper.sender {
  margin-left: auto;
  flex-direction: row-reverse;
}

.chat-bubble-wrapper.receiver {
  margin-right: auto;
}

.bubble-avatar {
  width: var(--avatar-size);
  height: var(--avatar-size);
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color) 0%, #5856d6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: var(--bubble-shadow);
  transition: all 0.3s ease;
}

.bubble-avatar:hover {
  transform: scale(1.05);
  box-shadow: var(--bubble-shadow-hover);
}

.chat-bubble-wrapper.sender .bubble-avatar {
  margin-left: 12px;
}

.chat-bubble-wrapper.receiver .bubble-avatar {
  margin-right: 12px;
}

.chat-bubble {
  padding: 14px 18px;
  border-radius: var(--bubble-border-radius);
  position: relative;
  background: var(--receiver-bg);
  color: var(--receiver-text-color);
  box-shadow: var(--bubble-shadow);
  min-width: 60px;
  word-wrap: break-word;
  white-space: pre-wrap;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.chat-bubble:hover {
  transform: translateY(-1px);
  box-shadow: var(--bubble-shadow-hover);
}

.chat-bubble.has-tail::before {
  content: "";
  position: absolute;
  bottom: 8px;
  width: 0;
  height: 0;
  border: 8px solid transparent;
}

/* Sender bubble styling */
.sender .chat-bubble {
  background: var(--sender-bg);
  color: var(--sender-text-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.sender .chat-bubble.has-tail::before {
  right: -8px;
  border-left-color: #007AFF;
  border-right-width: 0;
  border-top-color: #007AFF;
  border-bottom-color: transparent;
}

/* Receiver bubble styling */
.receiver .chat-bubble {
  background: var(--receiver-bg);
}

.receiver .chat-bubble.has-tail::before {
  left: -8px;
  border-right-color: rgba(255, 255, 255, 0.9);
  border-left-width: 0;
  border-top-color: rgba(255, 255, 255, 0.9);
  border-bottom-color: transparent;
}

.message-text {
  margin: 0 0 8px 0;
  font-size: 1rem;
  line-height: 1.6;
  font-weight: 500;
  letter-spacing: -0.2px;
}

.message-time {
  font-size: 0.75rem;
  color: var(--text-color-secondary);
  display: block;
  text-align: right;
  margin-top: 6px;
  opacity: 0.8;
  font-weight: 500;
}

/* Enhanced time styling for sender */
.sender .message-time {
  color: rgba(255, 255, 255, 0.8);
}

/* Add subtle animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .chat-bubble-wrapper {
    max-width: 90%;
    margin-bottom: 16px;
  }
  
  .chat-bubble {
    padding: 12px 16px;
  }
  
  .bubble-avatar {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
  
  .message-text {
    font-size: 0.95rem;
  }
}
</style>