<template>
  <div class="chat-page">
    <header class="chat-header">
      <button @click="goBack" class="back-button" aria-label="返回">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </button>
      <div class="rider-info" @click="navigateToRiderProfile" :class="{ 'clickable': chatInfo?.rider?.id }">
        <img
          v-if="chatInfo?.rider?.avatar"
          :src="chatInfo.rider.avatar"
          alt="Rider Avatar"
          class="rider-avatar-header"
        />
        <div v-else-if="chatInfo?.rider" class="rider-avatar-placeholder-header">
          {{ chatInfo.rider.name?.charAt(0) || 'R' }}
        </div>
        <h2 class="rider-name-header">{{ chatInfo?.rider?.name || '加载中...' }}</h2>
      </div>
      <div class="header-actions-placeholder"></div> <!-- Balances the back button for centering -->
    </header>

    <div v-if="isLoading" class="status-message loading">
      <div class="spinner"></div>
      加载聊天记录...
    </div>
    <div v-else-if="!chatInfo || !messages.length && !chatInfo.rider" class="status-message error">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
      无法加载聊天信息。
    </div>
    <div v-else-if="messages.length === 0 && chatInfo.rider" class="status-message empty">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><message-square></message-square></svg>
      还没有消息，开始聊天吧！
    </div>

    <div v-else class="messages-container" ref="messagesContainerRef">
      <ChatBubble
        v-for="message in messages"
        :key="message.id"
        :message="message"
        :is-sender="message.sender === 'user'"
        :rider-avatar="message.sender === 'rider' ? chatInfo?.rider?.avatar : undefined"
        :rider-name-initial="message.sender === 'rider' ? chatInfo?.rider?.name?.charAt(0) : undefined"
      />
    </div>

    <footer class="chat-input-area">
      <input
        type="text"
        v-model="newMessage"
        placeholder="输入消息..."
        @keyup.enter="sendMessage"
        class="message-input"
      />
      <button @click="sendMessage" :disabled="!newMessage.trim()" class="send-button" aria-label="发送">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
      </button>
    </footer>
  </div>
</template>

<script setup>
// ... (your existing script setup, but make sure fetchChatDetails is updated as above)
// Ensure you import ChatBubble, ref, onMounted, nextTick, watch, useRoute, useRouter
import { ref, onMounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ChatBubble from '@/components/Message/ChatBubble.vue';

const route = useRoute();
const router = useRouter();

const props = defineProps({
  chatId: {
    type: String,
    required: true,
  },
});

const chatInfo = ref(null);
const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(true);
const messagesContainerRef = ref(null);

const fetchChatDetails = async (id) => {
  // ... (implementation from section I.2) ...
  isLoading.value = true;
  chatInfo.value = null; 
  messages.value = [];   

  try {
    const response = await fetch('/data/messages.json'); 
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const allChatsData = await response.json();
    const currentChatData = allChatsData[id];

    if (currentChatData) {
      chatInfo.value = {
        id: id,
        rider: currentChatData.rider,
      };
      messages.value = currentChatData.messages.map(msg => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }));
    } else {
      console.error(`Chat with id ${id} not found in messages.json`);
    }
  } catch (error) {
    console.error("Failed to fetch chat details:", error);
  } finally {
    isLoading.value = false;
    await nextTick(); 
    scrollToBottom();
  }
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;
  const message = {
    id: `msg_${Date.now()}`,
    text: newMessage.value,
    sender: 'user',
    timestamp: new Date(),
  };
  messages.value.push(message);
  newMessage.value = '';
  scrollToBottom();
  // console.log('Sending message:', message); // For real app, send to backend
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainerRef.value) {
      messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight;
    }
  });
};

const goBack = () => {
  router.back();
};

const navigateToRiderProfile = () => {
  if (chatInfo.value?.rider?.id) {
    router.push({ name: 'RiderProfilePage', params: { riderId: chatInfo.value.rider.id } });
  }
};

onMounted(() => {
  fetchChatDetails(props.chatId);
});

watch(() => props.chatId, (newChatId) => {
  if (newChatId) {
    fetchChatDetails(newChatId);
  }
});
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 720px; /* Full viewport height */
  max-width: 500px; /* Max width for chat interface */
  margin: 0 auto; /* Center on larger screens */
  background-color: #f0f2f5; /* A slightly off-white background */
  border-left: 1px solid #e0e0e0; /* Optional border */
  border-right: 1px solid #e0e0e0; /* Optional border */
  box-shadow: 0 0 10px rgba(0,0,0,0.05); /* Subtle shadow */
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  flex-shrink: 0; /* Prevent header from shrinking */
}

.back-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  padding: 8px;
  margin-right: 8px; /* Space between button and title */
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
.back-button:hover {
  background-color: #f0f0f0;
}
.back-button svg {
  width: 22px;
  height: 22px;
  stroke: #555;
}

.rider-info {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: center; /* Center content within this div */
  min-width: 0; /* Allow rider name to truncate */
}
.rider-info.clickable {
  cursor: pointer;
}

.rider-avatar-header {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
  background-color: #e0e0e0; /* Placeholder bg */
}
.rider-avatar-placeholder-header {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
  background-color: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
}

.rider-name-header {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-actions-placeholder {
  width: 40px; /* Approximate width of back button + margin for balance */
  flex-shrink: 0;
}

.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #e5ddd5; /* WhatsApp-like background */
  /* background-image: url('/path/to/your/chat-bg.png'); /* Optional background image */
}
/* Custom scrollbar (optional, webkit only) */
.messages-container::-webkit-scrollbar {
  width: 6px;
}
.messages-container::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
  border-radius: 3px;
}

.status-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1; /* Take up space if messages are empty */
  padding: 2rem;
  color: #666;
  font-size: 0.9rem;
  text-align: center;
}
.status-message svg {
  width: 32px;
  height: 32px;
  margin-bottom: 10px;
  stroke: #888;
}
.loading .spinner {
  border: 4px solid #f3f3f3; /* Light grey */
  border-top: 4px solid #007bff; /* Blue */
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


.chat-input-area {
  position: fixed;
  display: flex;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 470px; /* Match page max-width */
  margin: 0 auto; /* Center it */
  align-items: center;
  padding: 10px 16px;
  border-top: 1px solid #e0e0e0;
  background-color: #f8f9fa;
  flex-shrink: 0; /* Prevent input area from shrinking */
}

.message-input {
  flex-grow: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  margin-right: 10px;
  font-size: 1rem;
  outline: none;
}
.message-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.send-button {
  padding: 8px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%; /* Make it circular */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px; /* Fixed width */
  height: 40px; /* Fixed height */
  transition: background-color 0.2s ease;
}
.send-button svg {
  width: 20px;
  height: 20px;
}
.send-button:hover:not(:disabled) {
  background-color: #0056b3;
}
.send-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}
</style>