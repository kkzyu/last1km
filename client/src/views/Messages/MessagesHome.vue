<template>
  <div class="messages-home">
    <MessagesHeader 
      :has-unread-messages="hasUnreadMessages"
      @mark-all-read="markAllAsRead"
    />

    <LoadingSpinner v-if="isLoading" />
    <EmptyState v-else-if="chatList.length === 0" />
    
    <ul v-else class="chat-list">
      <MessageListItem
        v-for="chat in sortedChatList"
        :key="chat.id"
        :chat="chat"
        @click="navigateToChat(chat.id)"
      />
    </ul>
    <BottomNav />
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import riders from '@/assets/data/riders.json'
import chats from '@/assets/data/chats.json'
import MessagesHeader from '@/components/Header/MessagesHead.vue'
import MessageListItem from '@/components/Message/MessageListItem.vue'
import LoadingSpinner from '@/components/UI/LoadingSpinner.vue'
import EmptyState from '@/components/UI/EmptyState.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

const router = useRouter()
const chatList = ref([])
const isLoading = ref(true)

const fetchChatList = async () => {
  isLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  chatList.value = chats.map(chat => ({
    ...chat,
    rider: riders.find(r => r.id === chat.riderId),
    timestamp: new Date(Date.now() - chat.minutesAgo * 60 * 1000).toISOString()
  }))

  isLoading.value = false
};

// 保持原有计算属性和方法不变
const sortedChatList = computed(() => {
  return [...chatList.value].sort((a, b) => 
    new Date(b.timestamp) - new Date(a.timestamp)
  )
})

const hasUnreadMessages = computed(() => {
  return chatList.value.some(chat => chat.unreadCount > 0)
});

onMounted(() => {
  fetchChatList();
});

const markAllAsRead = () => {
  chatList.value.forEach(chat => {
    chat.unreadCount = 0;
  });
  // 在实际应用中，这里会调用API通知后端
  console.log('所有消息已标记为已读');
};

const navigateToChat = (chatId) => {
  // 导航前可以将该聊天的未读消息清零
  const chat = chatList.value.find(c => c.id === chatId);
  if (chat) {
    chat.unreadCount = 0;
  }
  router.push({ name: 'chat', params: { chatId } });
};
</script>
<style scoped>


.chat-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.loading, .empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
}
</style>