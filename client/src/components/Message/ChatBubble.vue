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

// ... existing template and script ...
<style scoped>
/* Unified theme colors (example, adjust as needed) */
:root {
  --primary-color: #007AFF; /* Modern iOS Blue, can be used for avatar fallback bg */
  --sender-bg: #007AFF;    /* Sender bubble background */
  --sender-text-color: #FFFFFF; /* Text color for sender messages */
  --receiver-bg: #EFEFEF;  /* Light grey for receiver */
  --receiver-text-color: #1C1C1E; /* Darker text for better contrast on light grey receiver bubble */
  --text-color-secondary: #8A8A8E; /* For timestamps on receiver, other secondary info */
  --bubble-border-radius: 16px; /* Softer, more rounded corners */
  --avatar-size: 36px;
}

.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 16px;
  max-width: 80%;
  align-items: flex-end;
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
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  flex-shrink: 0;
}

.chat-bubble-wrapper.sender .bubble-avatar {
  margin-left: 10px;
}

.chat-bubble-wrapper.receiver .bubble-avatar {
  margin-right: 10px;
}

.chat-bubble {
  padding: 10px 15px;
  border-radius: var(--bubble-border-radius);
  position: relative;
  background-color: var(--receiver-bg); /* Default for receiver */
  color: var(--receiver-text-color);    /* Default text color for receiver */
  box-shadow: 0 1px 3px rgba(0,0,0,0.06); /* Softer, more subtle shadow */
  min-width: 50px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.chat-bubble.has-tail::before {
  content: "";
  position: absolute;
  bottom: 0px;
  width: 0;
  height: 0;
  border: 7px solid transparent; /* Slightly smaller tail */
  transform: translateY(-1px); /* Adjusted for new size and smoother look */
}

/* Sender bubble styling */
.sender .chat-bubble {
  background-color: var(--sender-bg);
  color: var(--sender-text-color); /* Ensure text is readable on sender background */
}
.sender .chat-bubble.has-tail::before {
  right: -8px; /* Adjusted position for smaller tail */
  border-left-color: var(--sender-bg);
  border-right-width: 0;
  border-top-color: var(--sender-bg);
  border-bottom-color: transparent;
}

/* Receiver bubble styling */
.receiver .chat-bubble {
 background-color: var(--receiver-bg);
 /* Text color is var(--receiver-text-color) by default from .chat-bubble */
}
.receiver .chat-bubble.has-tail::before {
  left: -8px; /* Adjusted position for smaller tail */
  border-right-color: var(--receiver-bg);
  border-left-width: 0;
  border-top-color: var(--receiver-bg);
  border-bottom-color: transparent;
}

.message-content {
  /* Styles for the main text content area if needed */
}

.message-text {
  margin: 0 0 5px 0;
  font-size: 0.9rem;
  line-height: 1.5;
  /* Color is inherited from .chat-bubble or .sender .chat-bubble */
}

.message-time {
  font-size: 0.7rem;
  color: var(--text-color-secondary); /* Default for receiver */
  display: block;
  text-align: right;
  margin-top: 4px;
  opacity: 0.8;
}

/* Specific time color for sender to ensure readability on dark background */
.sender .message-time {
  color: rgba(255, 255, 255, 0.75); /* Semi-transparent white for time on sender bubble */
}
</style>