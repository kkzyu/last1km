import { defineStore } from 'pinia';
import { nextTick } from 'vue';
import { messageAPI } from '@/api/api.js';

// Fallback for BASE_URL if not defined by Vite/environment
const BASE_URL = import.meta.env.BASE_URL || '/';

// 模拟骑手回复列表
const RIDER_REPLIES = [
    "好的，我马上到！",
    "请稍等，大约5分钟后到达。",
    "我已经在路上了。",
    "请问具体在哪个位置？",
    "感谢您的耐心等待。",
    "我找不到具体位置，能发个定位吗？",
    "收到，马上处理。",
    "没问题。"
];

// Helper function to resolve asset paths correctly with the base URL
const resolveAssetPath = (relativePath) => {
    if (!relativePath) return undefined;
    // Ensure BASE_URL ends with a slash if it's not just '/'
    const SANE_BASE_URL = (BASE_URL === '/' || BASE_URL.endsWith('/')) ? BASE_URL : `${BASE_URL}/`;

    let path = relativePath;
    // Remove leading slash from relativePath if SANE_BASE_URL is more than just '/'
    // and relativePath starts with '/' to avoid double slashes like '/basename//path'.
    // If SANE_BASE_URL is '/', then '/path' is fine.
    if (SANE_BASE_URL.length > 1 && path.startsWith('/')) {
        path = path.substring(1);
    }
    // For paths like 'data/messages.json' ensure they are not prefixed with an extra slash if not needed.
    if (SANE_BASE_URL.endsWith('/') && path.startsWith('/')) {
        return `${SANE_BASE_URL}${path.substring(1)}`;
    }
    return `${SANE_BASE_URL}${path}`;
};

export const useChatStore = defineStore('chat', {
    state: () => ({
        chatInfo: null, // { id: string, rider: { id: string, name: string, avatar?: string } | null }
        messages: [], // Array of message objects { id, text, sender, timestamp }
        newMessage: '',
        isLoading: true,
        currentChatId: null,
        error: null, // To store any error messages during fetch
    }),
    actions: {
        setCurrentChatId(chatId) {
            this.currentChatId = chatId;
        },        async fetchChatDetails(chatId) {
            if (!chatId) {
                this.isLoading = false;
                this.error = "聊天ID无效。";
                console.error("fetchChatDetails called with no chatId");
                return;
            }
            this.isLoading = true;
            this.error = null;
            // Reset previous chat data
            this.chatInfo = null;
            this.messages = [];

            try {
                const response = await messageAPI.getChatDetails(chatId);
                const chatData = response.data; // API响应通常包装在data属性中
                
                if (chatData) {
                    const riderData = chatData.rider ? {
                        ...chatData.rider,
                        avatar: chatData.rider.avatar ? resolveAssetPath(chatData.rider.avatar) : undefined
                    } : null;

                    this.chatInfo = {
                        id: chatId,
                        rider: riderData,
                    };

                    // 确保messages存在且是数组
                    const messages = chatData.messages || [];
                    this.messages = messages.map(msg => ({
                        ...msg,
                        timestamp: new Date(msg.timestamp)
                    })).sort((a, b) => a.timestamp - b.timestamp);

                    if (this.messages.length === 0 && this.chatInfo?.rider) {
                        this.simulateWelcomeMessage();
                    }
                } else {
                    console.error(`Chat with id ${chatId} not found`);
                    this.error = `无法找到ID为 ${chatId} 的聊天记录。`;
                    this.chatInfo = { id: chatId, rider: null };
                }            } catch (error) {
                console.error("Failed to fetch chat details:", error);
                // 检查是否是404错误（聊天记录不存在）
                if (error.response?.status === 404) {
                    // 尝试创建空聊天状态，显示"暂无聊天记录"
                    this.chatInfo = { id: chatId, rider: null };
                    this.messages = [];
                    this.error = null; // 不显示错误，而是显示空状态
                } else {
                    this.error = `加载聊天详情失败: ${error.message}`;
                    this.chatInfo = { id: chatId, rider: null };
                }
            } finally {
                this.isLoading = false;
            }
        },

        simulateWelcomeMessage() {
            if (!this.chatInfo?.rider) return;
            const welcomeMsg = {
                id: `msg_welcome_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
                text: `您好，我是骑手 ${this.chatInfo.rider.name}，请问有什么可以帮助您的吗？`,
                sender: 'rider',
                timestamp: new Date(),
            };
            this.messages.push(welcomeMsg);
        },        async sendMessage(currentUserId = 'user') {
            if (!this.newMessage.trim()) return;
            if (!this.chatInfo && !this.currentChatId) {
                console.warn("Cannot send message, no chat context.");
                this.error = "无法发送消息：未找到聊天对象。";
                return;
            }

            const messageText = this.newMessage.trim();
            this.newMessage = '';

            try {
                // Use backend API to send message
                const chatId = this.currentChatId || this.chatInfo.id;
                const response = await messageAPI.sendMessage(chatId, messageText);
                
                if (response.data && response.data.success) {
                    // Add the sent message to local state
                    const message = {
                        id: `msg_user_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
                        text: messageText,
                        sender: currentUserId,
                        timestamp: new Date(),
                    };
                    this.messages.push(message);

                    if (this.chatInfo?.rider) {
                        this.simulateReply(messageText);
                    }
                }
            } catch (error) {
                console.error("Failed to send message:", error);
                this.error = `发送消息失败: ${error.message}`;
                // Restore the message text so user can try again
                this.newMessage = messageText;
            }
        },

        simulateReply(userMessageText = "") {
            const delay = 1000 + Math.random() * 1500;

            setTimeout(() => {
                let replyText = RIDER_REPLIES[Math.floor(Math.random() * RIDER_REPLIES.length)];

                if (userMessageText.toLowerCase().includes("位置") && !replyText.includes("位置")) {
                    replyText = "请问您的具体位置是？我好导航过去。";
                } else if (userMessageText.toLowerCase().includes("你好") || userMessageText.toLowerCase().includes("您好")) {
                    replyText = "您好！有什么可以帮到您？";
                }

                const reply = {
                    id: `msg_rider_reply_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
                    text: replyText,
                    sender: 'rider',
                    timestamp: new Date(),
                };
                this.messages.push(reply);
            }, delay);
        },
    },
    getters: {
        riderName: (state) => state.chatInfo?.rider?.name || '骑手',
        riderAvatar: (state) => state.chatInfo?.rider?.avatar,
        riderId: (state) => state.chatInfo?.rider?.id,
        sortedMessages: (state) => state.messages, // Messages are sorted on fetch
        isLoadingChat: (state) => state.isLoading,
        chatError: (state) => state.error,

        // Getter for ChatBubble to use, providing initials if no avatar
        getReceiverAvatar: (state) => state.chatInfo?.rider?.avatar,
        getReceiverNameInitial: (state) => {
            return state.chatInfo?.rider?.name?.charAt(0).toUpperCase() || 'R';
        }
    }
}); 