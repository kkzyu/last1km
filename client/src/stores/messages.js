import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import ridersData from '@/assets/data/riders.json';
import chatsData from '@/assets/data/chats.json';

export const useMessagesStore = defineStore('messages', () => {
    const router = useRouter();

    const chatList = ref([]);
    const isLoading = ref(true);

    const fetchChatList = async () => {
        isLoading.value = true;
        // 模拟 API 调用
        await new Promise(resolve => setTimeout(resolve, 1000));

        chatList.value = chatsData.map(chat => {
            const rider = ridersData.find(r => r.id === chat.riderId);
            return {
                ...chat,
                rider: rider || { id: chat.riderId, name: '未知骑手', avatar: '/avatars/default.png' }, // 提供骑手数据缺失时的默认值
                timestamp: new Date(Date.now() - chat.minutesAgo * 60 * 1000).toISOString(),
            };
        });
        isLoading.value = false;
    };

    const sortedChatList = computed(() => {
        return [...chatList.value].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    });

    const hasUnreadMessages = computed(() => {
        return chatList.value.some(chat => chat.unreadCount > 0);
    });

    const markAllAsRead = () => {
        chatList.value.forEach(chat => {
            if (chat.unreadCount > 0) {
                chat.unreadCount = 0;
            }
        });
        // 实际应用中应有 API 调用
        console.log('所有消息已通过 Pinia 标记为已读');
    };

    const markChatAsRead = (chatId) => {
        const chat = chatList.value.find(c => c.id === chatId);
        if (chat && chat.unreadCount > 0) {
            chat.unreadCount = 0;
            // 实际应用中应有 API 调用
            console.log(`聊天 ${chatId} 已通过 Pinia 标记为已读`);
        }
    };

    const navigateToChat = (chatId) => {
        markChatAsRead(chatId); // 导航前标记为已读
        router.push({ name: 'chat', params: { chatId } });
    };

    // 组件挂载时自动获取数据
    // onMounted(() => { // Pinia store 的 setup 函数中不能直接用 onMounted，需要在组件中调用 fetchChatList
    //   fetchChatList();
    // });

    return {
        chatList,
        isLoading,
        fetchChatList,
        sortedChatList,
        hasUnreadMessages,
        markAllAsRead,
        navigateToChat,
    };
}); 