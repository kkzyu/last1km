<template>
  <a-layout class="chat-page-layout">
    <a-layout-header class="chat-header">
      <a-button type="text" @click="goBack" class="back-button" aria-label="返回">
        <template #icon><ArrowLeftOutlined /></template>
      </a-button>
      <div class="rider-info" @click="navigateToRiderProfile" :class="{ 'clickable': !!chatStore.riderId }">
        <a-avatar :size="40" :src="chatStore.riderAvatar" class="rider-avatar-header">
          {{ chatStore.riderName?.charAt(0) || 'R' }}
        </a-avatar>
        <span class="rider-name-header">{{ chatStore.riderName || '加载中...' }}</span>
      </div>
      <!-- Placeholder for potential future icons like more_vert -->
      <div class="header-actions-placeholder"></div>
    </a-layout-header>

    <a-layout-content class="messages-layout-content">      <div v-if="chatStore.isLoadingChat" class="status-message loading">
        <a-spin size="large" />
        <p>加载聊天记录中...</p>
      </div>
      <div v-else-if="chatStore.chatError" class="status-message error">
        <a-alert :message="chatStore.chatError" type="error" show-icon />
      </div>
      <div v-else-if="!chatStore.sortedMessages.length && chatStore.chatInfo?.rider" class="status-message empty">
        <a-empty description="还没有消息，开始聊天吧！" />
      </div>
      <div v-else-if="!chatStore.sortedMessages.length && chatStore.chatInfo && !chatStore.chatInfo.rider" class="status-message empty">
        <a-empty description="暂无聊天记录" />
      </div>
      <div v-else-if="!chatStore.chatInfo && !chatStore.isLoadingChat && !chatStore.chatError" class="status-message empty">
         <a-empty description="暂无聊天记录" />
      </div>
      
      <div class="messages-container" ref="messagesContainerRef" v-show="chatStore.sortedMessages.length > 0">
        <ChatBubble
          v-for="message in chatStore.sortedMessages"
          :key="message.id"
          :message="message"
          :is-sender="message.sender === 'user'" 
          :avatar-src="message.sender === 'rider' ? chatStore.getReceiverAvatar : undefined"
          :name-initial="message.sender === 'rider' ? chatStore.getReceiverNameInitial : undefined"
        />
      </div>
    </a-layout-content>

    <a-layout-footer class="chat-input-area" v-if="chatStore.chatInfo?.rider">
      <a-input
        v-model:value="chatStore.newMessage"
        placeholder="输入消息..."
        @pressEnter="handleSendMessage"
        class="message-input"
        size="large"
      />
      <a-button
        type="primary"
        @click="handleSendMessage"
        :disabled="!chatStore.newMessage.trim() || !chatStore.chatInfo?.rider"
        class="send-button"
        aria-label="发送"
        size="large"
      >
        <template #icon><SendOutlined /></template>
      </a-button>
    </a-layout-footer>
    <a-layout-footer class="chat-input-area disabled-input-area" v-else-if="!chatStore.isLoadingChat">
        <a-input placeholder="无法与骑手聊天" disabled size="large" />
        <a-button type="primary" disabled size="large">
            <template #icon><SendOutlined /></template>
        </a-button>
    </a-layout-footer>
  </a-layout>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useChatStore } from '@/stores/chatStore';
import ChatBubble from '@/components/Message/ChatBubble.vue';
import {
  Layout as ALayout,
  LayoutHeader as ALayoutHeader,
  LayoutContent as ALayoutContent,
  LayoutFooter as ALayoutFooter,
  Button as AButton,
  Avatar as AAvatar,
  Input as AInput,
  Spin as ASpin,
  Empty as AEmpty,
  Alert as AAlert
} from 'ant-design-vue';
import { ArrowLeftOutlined, SendOutlined } from '@ant-design/icons-vue';

const route = useRoute();
const router = useRouter();
const chatStore = useChatStore();

const props = defineProps({
  chatId: {
    type: String,
    required: true,
  },
});

// Make store state and getters reactive using storeToRefs
// const { newMessage, isLoadingChat, chatError, sortedMessages, chatInfo, getReceiverAvatar, getReceiverNameInitial } = storeToRefs(chatStore);

const messagesContainerRef = ref(null);

const scrollToBottom = (behavior = 'smooth') => {
  nextTick(() => {
    if (messagesContainerRef.value) {
      messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight;
    }
  });
};

const handleSendMessage = () => {
  chatStore.sendMessage('user'); 
};

const goBack = () => {
  router.back();
};

const navigateToRiderProfile = () => {
  if (chatStore.riderId) {
    router.push({ name: 'rider-profile', params: { riderId: chatStore.riderId } });
  }
};

onMounted(() => {
  chatStore.setCurrentChatId(props.chatId);
  chatStore.fetchChatDetails(props.chatId);
});

watch(() => props.chatId, (newChatId) => {
  if (newChatId) {
    chatStore.setCurrentChatId(newChatId);
    chatStore.fetchChatDetails(newChatId);
  } else {
    // Handle case where chatId becomes invalid or null
    chatStore.isLoading = false;
    chatStore.error = "无效的聊天会话。";
    chatStore.messages = [];
    chatStore.chatInfo = null;
  }
});

// Watch for new messages and scroll to bottom
watch(() => chatStore.sortedMessages, (newMessages, oldMessages) => {
  if (newMessages.length !== oldMessages.length) {
    scrollToBottom();
  }
}, { deep: true });

// Scroll to bottom when loading finishes and there are messages
watch(() => chatStore.isLoadingChat, (loading) => {
    if(!loading && chatStore.sortedMessages.length > 0) {
        scrollToBottom('auto'); // instant scroll on initial load
    }
});

</script>

<style scoped>
/* Modern Chat Theme Variables */
:root {
  --chat-primary-color: #007AFF; /* iOS Blue */
  --chat-primary-light: #E3F2FD;
  --chat-background-color: #F8F9FA; /* Subtle warm background */
  --chat-container-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Beautiful gradient */
  --chat-header-bg: rgba(255, 255, 255, 0.95); /* Semi-transparent header */
  --chat-footer-bg: rgba(255, 255, 255, 0.98);
  --chat-text-color: #1a1a1a;
  --chat-border-color: rgba(0, 0, 0, 0.08);
  --chat-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  --modern-max-width: 440px;
  --border-radius: 16px;
  --border-radius-small: 12px;
}

.chat-page-layout {
  height: 100vh; /* Full viewport height */
  max-width: var(--modern-max-width);
  margin: 0 auto; /* Center on larger screens */
  background: var(--chat-container-bg);
  display: flex;
  flex-direction: column;
  box-shadow: var(--chat-shadow);
  border-radius: var(--border-radius);
  overflow: hidden;
  backdrop-filter: blur(20px);
  position: relative;
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  background: var(--chat-header-bg);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--chat-border-color);
  height: 80px;
  flex-shrink: 0;
  justify-content: space-between;
  position: relative;
  z-index: 10;
}

.back-button {
  color: var(--chat-text-color) !important;
  margin-right: 16px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-button:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.back-button .anticon {
  font-size: 20px;
  font-weight: 600;
}

.rider-info {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: flex-start;
  overflow: hidden;
  padding: 0 12px;
  transition: all 0.3s ease;
}

.rider-info.clickable {
  cursor: pointer;
  border-radius: var(--border-radius-small);
  padding: 8px 12px;
}

.rider-info.clickable:hover {
  background: rgba(255, 255, 255, 0.6);
  transform: scale(1.02);
}

.rider-avatar-header {
  margin-right: 16px;
  flex-shrink: 0;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.rider-name-header {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--chat-text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.5px;
}

.header-actions-placeholder {
  width: 48px; /* To balance the back button area */
  flex-shrink: 0;
}

.messages-layout-content {
  flex-grow: 1;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  position: relative;
}

.messages-layout-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 206, 84, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(232, 121, 249, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.messages-container {
  padding: 24px 20px;
  height: 100%;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}

/* Modern scrollbar styling */
.messages-layout-content::-webkit-scrollbar, 
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-layout-content::-webkit-scrollbar-thumb, 
.messages-container::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(120, 119, 198, 0.3) 0%, rgba(255, 206, 84, 0.3) 100%);
  border-radius: 4px;
  border: 2px solid transparent;
  background-clip: content-box;
}

.messages-layout-content::-webkit-scrollbar-track, 
.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-layout-content::-webkit-scrollbar-thumb:hover, 
.messages-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(120, 119, 198, 0.5) 0%, rgba(255, 206, 84, 0.5) 100%);
}

.status-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 2rem;
  color: rgba(26, 26, 26, 0.6);
  flex-grow: 1;
  position: relative;
  z-index: 1;
}

.status-message.loading {
  background: rgba(255, 255, 255, 0.8);
  border-radius: var(--border-radius);
  margin: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.status-message.loading p {
  margin-top: 20px;
  font-size: 1rem;
  font-weight: 500;
  color: var(--chat-text-color);
}

.status-message.empty {
  background: rgba(255, 255, 255, 0.6);
  border-radius: var(--border-radius);
  margin: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.status-message .ant-alert {
  width: auto;
  max-width: 90%;
  border-radius: var(--border-radius-small);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}


.chat-input-area {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: var(--chat-footer-bg);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--chat-border-color);
  flex-shrink: 0;
  position: relative;
  z-index: 10;
  gap: 16px;
}

.chat-input-area.disabled-input-area .ant-input {
  cursor: not-allowed;
  background: rgba(0, 0, 0, 0.05);
}

.message-input {
  flex: 1;
  border-radius: 24px !important;
  border: 2px solid rgba(0, 122, 255, 0.1) !important;
  background: rgba(255, 255, 255, 0.9) !important;
  padding: 12px 20px !important;
  font-size: 16px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.message-input:focus {
  border-color: var(--chat-primary-color) !important;
  box-shadow: 0 4px 20px rgba(0, 122, 255, 0.2) !important;
  background: rgba(255, 255, 255, 1) !important;
}

.send-button {
  width: 48px !important;
  height: 48px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, var(--chat-primary-color) 0%, #5856d6 100%) !important;
  border: none !important;
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.3) !important;
  transition: all 0.3s ease !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05) !important;
  box-shadow: 0 8px 25px rgba(0, 122, 255, 0.4) !important;
}

.send-button:active:not(:disabled) {
  transform: translateY(0) scale(0.95) !important;
}

.send-button:disabled {
  background: rgba(0, 0, 0, 0.1) !important;
  box-shadow: none !important;
  cursor: not-allowed !important;
}

.send-button .anticon {
  font-size: 20px;
  color: white;
  font-weight: 600;
}

/* Hide scrollbar for cleaner look */
.messages-container::-webkit-scrollbar {
  display: none;
}

.messages-container {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Responsive Design */
@media (max-width: 480px) {
  .chat-page-layout {
    border-radius: 0;
    max-width: 100%;
    height: 100vh;
  }
  
  .chat-header {
    padding: 12px 16px;
    height: 70px;
  }
  
  .rider-name-header {
    font-size: 1.1rem;
  }
  
  .messages-container {
    padding: 20px 16px;
  }
  
  .chat-input-area {
    padding: 16px 16px 20px;
    gap: 12px;
  }
  
  .back-button {
    width: 40px;
    height: 40px;
    margin-right: 12px;
  }
  
  .send-button {
    width: 44px !important;
    height: 44px !important;
  }
}

/* Add subtle animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-page-layout {
  animation: fadeInUp 0.5s ease-out;
}

/* Enhance focus states for accessibility */
.back-button:focus-visible,
.send-button:focus-visible {
  outline: 2px solid var(--chat-primary-color);
  outline-offset: 2px;
}

.message-input:focus-visible {
  outline: none;
}
</style>