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

    <a-layout-content class="messages-layout-content">
      <div v-if="chatStore.isLoadingChat" class="status-message loading">
        <a-spin size="large" />
        <p>加载聊天记录中...</p>
      </div>
      <div v-else-if="chatStore.chatError" class="status-message error">
        <a-alert :message="chatStore.chatError" type="error" show-icon />
      </div>
      <div v-else-if="!chatStore.sortedMessages.length && chatStore.chatInfo?.rider" class="status-message empty">
        <a-empty description="还没有消息，开始聊天吧！" />
      </div>
      <div v-else-if="!chatStore.chatInfo?.rider && !chatStore.isLoadingChat" class="status-message error">
         <a-empty description="无法加载骑手信息或聊天记录。" />
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
/* Theme variables (consider moving to a global CSS/SCSS file for Ant Design theming) */
:root {
  --chat-primary-color: #1890ff; /* Ant Design default blue */
  --chat-background-color: #f0f2f5; /* Light grey, common for app backgrounds */
  --chat-container-bg: #ffffff; /* Background for messages area */
  --chat-header-bg: #ffffff;
  --chat-footer-bg: #f8f9fa;
  --chat-text-color: #333333;
  --chat-border-color: #e8e8e8;
  --modern-max-width: 420px; /* Slightly wider for modern feel */
}

.chat-page-layout {
  height: 900px; /* Full viewport height */
  max-width: var(--modern-max-width);
  margin: 0 auto; /* Center on larger screens */
  background-color: var(--chat-background-color);
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-left: 1px solid var(--chat-border-color);
  border-right: 1px solid var(--chat-border-color);
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 0 16px;
  background-color: var(--chat-header-bg);
  border-bottom: 1px solid var(--chat-border-color);
  height: 64px;
  flex-shrink: 0;
  justify-content: space-between;
}

.back-button {
  color: var(--chat-text-color) !important;
  margin-right: 12px;
}
.back-button .anticon {
    font-size: 20px;
}

.rider-info {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: flex-start; /* Align items to the start */
  overflow: hidden; /* For text ellipsis */
  padding: 0 8px;
}
.rider-info.clickable {
  cursor: pointer;
}

.rider-avatar-header {
  margin-right: 12px;
  flex-shrink: 0;
}

.rider-name-header {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--chat-text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-actions-placeholder {
  width: 48px; /* To balance the back button area */
  flex-shrink: 0;
}

.messages-layout-content {
  flex-grow: 1;
  overflow-y: auto;
  background-color: var(--chat-container-bg); /* Use a clean background for messages */
  display: flex; /* Enable flex for status messages centering */
  flex-direction: column; /* Stack status messages or container */
}

.messages-container {
  padding: 20px 16px;
  height: 100%; /* Allow it to take full space for scrolling */
  overflow-y: auto;
}

/* Custom scrollbar for a cleaner look */
.messages-layout-content::-webkit-scrollbar, .messages-container::-webkit-scrollbar {
  width: 6px;
}
.messages-layout-content::-webkit-scrollbar-thumb, .messages-container::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.15);
  border-radius: 3px;
}
.messages-layout-content::-webkit-scrollbar-track, .messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.status-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  color: #888;
  flex-grow: 1; /* Center vertically */
}
.status-message.loading p {
    margin-top: 16px;
    font-size: 0.9rem;
}
.status-message .ant-alert {
    width: auto;
    max-width: 90%;
}


.chat-input-area {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-top: 1px solid var(--chat-border-color);
  background-color: var(--chat-footer-bg);
  flex-shrink: 0;
}
.chat-input-area.disabled-input-area .ant-input {
    cursor: not-allowed;
}

.message-input {
  margin-right: 12px;
  border-radius: 18px; /* Rounded input field */
}

.send-button .anticon {
  font-size: 18px;
}

.messages-container::-webkit-scrollbar {
  display: none;
}

/* Responsive adjustments if needed */
@media (max-width: 480px) {
  .chat-page-layout {
    border-left: none;
    border-right: none;
    box-shadow: none;
    max-width: 100%;
  }
  .chat-header {
    padding: 0 12px; /* Slightly less padding on mobile */
  }
  .rider-name-header {
    font-size: 1rem;
  }
  .messages-container {
    padding: 16px 12px;
  }
  .chat-input-area {
    padding: 10px 12px;
  }
}
</style>