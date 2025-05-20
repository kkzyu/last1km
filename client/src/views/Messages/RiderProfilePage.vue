<template>
  <div class="rider-profile-page">
    <header class="profile-header">
      <button @click="goBack" class="back-button">< 返回</button>
      <h1>骑手主页</h1>
      <div class="placeholder"></div>
    </header>

    <div v-if="isLoading" class="loading">加载骑手信息...</div>
    <div v-else-if="!riderInfo" class="error">无法加载骑手信息。</div>

    <div v-else class="profile-content">
      <img :src="riderInfo.avatar" :alt="riderInfo.name" class="rider-avatar" />
      <h2>{{ riderInfo.name }}</h2>
      <p><strong>ID:</strong> {{ riderInfo.id }}</p>
      <p><strong>评分:</strong> {{ riderInfo.rating }} / 5.0</p>
      <p><strong>车型:</strong> {{ riderInfo.vehicle }}</p>
      <p><strong>简介:</strong> {{ riderInfo.bio }}</p>
      <p><strong>已完成订单:</strong> {{ riderInfo.completedOrders }}</p>
      
      <!-- 假设我们知道与该骑手的聊天ID，或者可以根据riderId找到/创建聊天 -->
      <button v-if="riderInfo.chatId" @click="goToChat(riderInfo.chatId)" class="chat-button">
        继续聊天
      </button>
      <!-- 或者，如果没有直接的chatId，但可以发起新聊天 -->
      <!-- <button @click="startNewChat(riderInfo.id)" class="chat-button">
        发起聊天
      </button> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const props = defineProps({
  riderId: {
    type: String,
    required: true,
  },
});

const riderInfo = ref(null);
const isLoading = ref(true);

// 模拟API获取骑手信息
const fetchRiderProfile = async (id) => {
  isLoading.value = true;
  console.log(`Fetching profile for rider ${id}`);
  await new Promise(resolve => setTimeout(resolve, 500)); // 模拟网络延迟

  // 模拟数据
  const mockRiders = {
    'rider_123': {
      id: 'rider_123',
      name: '骑手小张',
      avatar: 'https://via.placeholder.com/150/FF0000/FFFFFF?Text=R1',
      rating: 4.8,
      vehicle: '电动车',
      bio: '五年配送经验，路线熟悉，服务热情。',
      completedOrders: 1250,
      chatId: 'chat_rider_123' // 假设我们知道与此骑手的聊天ID
    },
    'rider_456': {
      id: 'rider_456',
      name: '骑手李师傅',
      avatar: 'https://via.placeholder.com/150/00FF00/FFFFFF?Text=R2',
      rating: 4.9,
      vehicle: '摩托车',
      bio: '安全第一，准时送达。',
      completedOrders: 3000,
      chatId: 'chat_rider_456'
    },
    'rider_789': {
      id: 'rider_789',
      name: '骑手王美女',
      avatar: 'https://via.placeholder.com/150/0000FF/FFFFFF?Text=R3',
      rating: 4.7,
      vehicle: '电动车',
      bio: '微笑服务，送餐上门。',
      completedOrders: 800,
      chatId: 'chat_rider_789'
    }
  };

  riderInfo.value = mockRiders[id] || null;
  isLoading.value = false;
};

const goBack = () => {
  router.back();
};

const goToChat = (chatId) => {
  router.push({ name: 'ChatPage', params: { chatId } });
};

// const startNewChat = (riderId) => {
//   // 实际应用中，这里可能需要先通过API创建或获取一个chatId
//   console.log(`Attempting to start new chat with rider ${riderId}`);
//   // 假设创建后得到 chatId = 'new_chat_for_' + riderId;
//   // router.push({ name: 'ChatPage', params: { chatId: 'new_chat_for_' + riderId } });
// };

onMounted(() => {
  fetchRiderProfile(props.riderId);
});

watch(() => props.riderId, (newRiderId) => {
  if (newRiderId) {
    fetchRiderProfile(newRiderId);
  }
});
</script>

<style scoped>
.rider-profile-page {
  padding: 0 1rem 1rem 1rem;
  max-width: 600px;
  margin: 0 auto;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0; /* 调整内边距以适应无背景的头部 */
  margin-bottom: 1rem;
  border-bottom: 1px solid #e7e7e7;
}
.profile-header h1 {
  font-size: 1.2rem;
  margin: 0;
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
.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}
.profile-content {
  text-align: center;
}
.rider-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
  border: 3px solid #eee;
}
.profile-content h2 {
  font-size: 1.8rem;
  margin: 0.5rem 0;
}
.profile-content p {
  font-size: 1rem;
  color: #333;
  margin: 0.5rem 0;
  line-height: 1.6;
}
.chat-button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.chat-button:hover {
  background-color: #218838;
}
</style>