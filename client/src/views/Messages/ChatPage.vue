<template>
  <div class="chat-page">
    <header class="chat-header">
      <button @click="goBack" class="back-button">< 返回</button>
      <h2 @click="navigateToRiderProfile" class="rider-name-header">{{ chatInfo?.rider?.name || '加载中...' }}</h2>
      <div class="placeholder"></div> <!-- 占位使标题居中 -->
    </header>

    <div v-if="isLoading" class="loading">加载聊天记录...</div>
    <div v-else-if="!chatInfo" class="error">无法加载聊天信息。</div>
    
    <div v-else class="messages-container" ref="messagesContainerRef">
      <ChatBubble
        v-for="message in messages"
        :key="message.id"
        :message="message"
        :is-sender="message.sender === 'user'"
      />
    </div>

    <footer class="chat-input-area">
      <input
        type="text"
        v-model="newMessage"
        placeholder="输入消息..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage" :disabled="!newMessage.trim()">发送</button>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ChatBubble from '@/components/Message/ChatBubble.vue'; // 引入子组件

const route = useRoute();
const router = useRouter();

const props = defineProps({
  chatId: {
    type: String,
    required: true,
  },
});

const chatInfo = ref(null); // 包含骑手信息等
const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(true);
const messagesContainerRef = ref(null); // 用于滚动到底部

// 模拟API获取聊天详情和消息记录
const fetchChatDetails = async (id) => {
  isLoading.value = true;
  console.log(`Fetching chat details for ${id}`);
  await new Promise(resolve => setTimeout(resolve, 500)); // 模拟网络延迟

  // 模拟数据 - 实际应用中会根据 chatId 从后端获取
  if (id === 'chat_rider_123') {
    chatInfo.value = {
      id: 'chat_rider_123',
      rider: { id: 'rider_123', name: '骑手小张', avatar: '' },
    };
    messages.value = [
      { id: 'msg1', text: '您好，您的订单已接单，正在火速赶往商家。', sender: 'rider', timestamp: new Date(Date.now() - 1000 * 60 * 10) },
      { id: 'msg2', text: '好的，谢谢！', sender: 'user', timestamp: new Date(Date.now() - 1000 * 60 * 9) },
      { id: 'msg3', text: '您的餐品已送达，请查收！', sender: 'rider', timestamp: new Date(Date.now() - 1000 * 60 * 5) },
    ];
  } else if (id === 'chat_rider_456') {
     chatInfo.value = {
      id: 'chat_rider_456',
      rider: { id: 'rider_456', name: '骑手李师傅', avatar: '' },
    };
    messages.value = [
      { id: 'msg4', text: '我还有5分钟到达。', sender: 'rider', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2) },
    ];
  } else if (id === 'chat_rider_789') {
     chatInfo.value = {
      id: 'chat_rider_789',
      rider: { id: 'rider_789', name: '骑手王美女', avatar: '' },
    };
    messages.value = [
      { id: 'msg5', text: '请问有什么忌口吗？', sender: 'rider', timestamp: new Date(Date.now() - 1000 * 60 * 32) },
      { id: 'msg6', text: '没有，谢谢。', sender: 'user', timestamp: new Date(Date.now() - 1000 * 60 * 31) },
      { id: 'msg7', text: '好的，马上为您加急。', sender: 'rider', timestamp: new Date(Date.now() - 1000 * 60 * 30) },
    ];
  } else {
    chatInfo.value = null;
    messages.value = [];
  }
  isLoading.value = false;
  scrollToBottom();
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;
  const message = {
    id: `msg_${Date.now()}`, // 临时ID
    text: newMessage.value,
    sender: 'user', // 假设当前用户是 'user'
    timestamp: new Date(),
  };
  messages.value.push(message);
  newMessage.value = '';
  scrollToBottom();
  // 在实际应用中，这里会调用API发送消息到后端
  console.log('Sending message:', message);
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainerRef.value) {
      messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight;
    }
  });
};

const goBack = () => {
  router.back(); // 或者 router.push({ name: 'MessagesHome' });
};

const navigateToRiderProfile = () => {
  if (chatInfo.value?.rider?.id) {
    router.push({ name: 'RiderProfilePage', params: { riderId: chatInfo.value.rider.id } });
  }
};

onMounted(() => {
  fetchChatDetails(props.chatId);
});

// 如果 chatId 变化 (例如通过浏览器前进后退在不同聊天间切换)，重新加载数据
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
  height: 100vh; /* 或根据你的布局调整 */
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ccc; /* 仅为演示 */
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f8f8f8;
  border-bottom: 1px solid #e7e7e7;
}
.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
  cursor: pointer;
}
.back-button {
  background: none;
  border: none;
  font-size: 1rem;
  color: #007bff;
  cursor: pointer;
  padding: 0.5rem;
}
.placeholder {
  width: 60px; /* 与返回按钮宽度近似，用于居中标题 */
}
.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #e5ddd5; /* 类似微信的背景色 */
}
.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}
.chat-input-area {
  display: flex;
  padding: 0.5rem;
  border-top: 1px solid #e7e7e7;
  background-color: #f0f0f0;
}
.chat-input-area input {
  flex-grow: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 20px;
  margin-right: 0.5rem;
}
.chat-input-area button {
  padding: 0.75rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}
.chat-input-area button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}
</style>