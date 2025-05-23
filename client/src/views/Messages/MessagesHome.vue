<template>
  <div class="messages-home">
    <MessagesHeader 
      :has-unread-messages="messagesStore.hasUnreadMessages"
      @mark-all-read="messagesStore.markAllAsRead"
    />

    <a-spin :spinning="messagesStore.isLoading" tip="加载中...">
      <div v-if="!messagesStore.isLoading && messagesStore.sortedChatList.length === 0" class="empty-state-container">
        <a-empty description="暂无消息" />
      </div>
      <a-list
        v-else-if="!messagesStore.isLoading"
        class="chat-list"
        item-layout="horizontal"
        :data-source="messagesStore.sortedChatList"
      >
        <template #renderItem="{ item }">
          <MessageListItem
            :chat="item"
            @click="messagesStore.navigateToChat(item.id)"
          />
        </template>
      </a-list>
    </a-spin>
    <BottomNav />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMessagesStore } from '@/stores/messages';
import MessagesHeader from '@/components/Header/MessagesHead.vue';
import MessageListItem from '@/components/Message/MessageListItem.vue';
import BottomNav from '@/components/Bottom/BottomNav.vue';
import { List as AList, Spin as ASpin, Empty as AEmpty } from 'ant-design-vue';

const messagesStore = useMessagesStore();

onMounted(() => {
  messagesStore.fetchChatList();
});

</script>

<style scoped>
.messages-home {
  display: flex;
  flex-direction: column;
  height: 850px; /* 假设 BottomNav 高度为 50px */
  background-color: #f0f2f5; /* Ant Design 风格的背景色 */
}

.chat-list {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #fff;
}

.empty-state-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 100px - 50px); /* 减去 Header 和 BottomNav 的大致高度 */
}

/* 根据需要添加或调整样式 */
:deep(.ant-list-item) {
  padding: 12px 16px !important;
}
</style>