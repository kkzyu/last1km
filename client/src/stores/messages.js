import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { messageAPI } from '@/api/api';

export const useMessagesStore = defineStore('messages', () => {
    const router = useRouter();

    const chatList = ref([]);
    const isLoading = ref(true);
    const error = ref(null);

    const fetchChatList = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await messageAPI.getChatList();
            if (response.data && response.data.success) {
                chatList.value = response.data.data;
            } else {
                throw new Error(response.data?.message || '获取聊天列表失败');
            }
        } catch (err) {
            console.error('获取聊天列表失败:', err);
            error.value = err.message || '获取聊天列表失败';
            chatList.value = [];
        } finally {
            isLoading.value = false;
        }
    };

    const sortedChatList = computed(() => {
        return [...chatList.value].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    });

    const hasUnreadMessages = computed(() => {
        return chatList.value.some(chat => chat.unreadCount > 0);
    });    const markAllAsRead = async () => {
        try {
            const response = await messageAPI.markAllChatsAsRead();
            if (response.data && response.data.success) {
                // Update local state
                chatList.value.forEach(chat => {
                    if (chat.unreadCount > 0) {
                        chat.unreadCount = 0;
                    }
                });
                console.log('所有消息已标记为已读');
            }
        } catch (error) {
            console.error('标记所有消息为已读失败:', error);
        }
    };

    const markChatAsRead = async (chatId) => {
        try {
            const response = await messageAPI.markChatAsRead(chatId);
            if (response.data && response.data.success) {
                // Update local state
                const chat = chatList.value.find(c => c.id === chatId);
                if (chat && chat.unreadCount > 0) {
                    chat.unreadCount = 0;
                    console.log(`聊天 ${chatId} 已标记为已读`);
                }
            }
        } catch (error) {
            console.error(`标记聊天 ${chatId} 为已读失败:`, error);
        }
    };const navigateToChat = async (chatId) => {
        await markChatAsRead(chatId); // 导航前标记为已读
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