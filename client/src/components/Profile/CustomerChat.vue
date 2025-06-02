<template>
  <div class="chat-overlay" @click="handleOverlayClick">
    <div class="chat-app" @click.stop>
      <div class="chat-header">
        <div class="header-info">
          <div class="avatar">
            <i class="fas fa-user-tie"></i>
          </div>
          <div class="service-info">
            <h3>在线客服</h3>
            <span class="status online">在线</span>
          </div>
        </div>
        <button class="close-button" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="chat-container">
        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(message, index) in messages" 
            :key="index" 
            :class="['message', message.sender]"
          >
            <div class="message-content">
              {{ message.content }}
            </div>
            <div class="message-time">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
          
          <!-- 加载动画 -->
          <div v-if="loading" class="message ai">
            <div class="glass-loader">
              <div class="loader-text">客服正在回复...</div>
              <div class="wave-loader">
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-area" :class="{ disabled: loading }">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
            class="message-input"
            :disabled="loading"
          />
          <button @click="sendMessage" class="send-button" :disabled="loading">
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

// 定义事件
const emit = defineEmits(['close'])

const userInput = ref('')
const messages = ref([])
const messagesContainer = ref(null)
const loading = ref(false)

const API_URL = '/api/chat'

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return

  addMessage('user', userInput.value)
  const messageToSend = userInput.value
  userInput.value = ''
  loading.value = true
  
  try {
    const response = await axios.post(API_URL, {
      message: messageToSend,
      context: 'customer_service'
    })
    
    if (response.data && response.data.success && response.data.data && response.data.data.reply) {
      addMessage('ai', response.data.data.reply)
    } else if (response.data && response.data.reply) {
      addMessage('ai', response.data.reply)
    } else {
      addMessage('ai', '抱歉，客服暂时无法回复，请稍后再试或拨打客服热线：400-123-4567')
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    let errorMessage = '网络连接异常，请检查网络或拨打客服热线：400-123-4567'
    
    if (error.response) {
      // 服务器响应了错误状态码
      if (error.response.status === 404) {
        errorMessage = '客服服务暂时不可用，请稍后再试'
      } else if (error.response.status >= 500) {
        errorMessage = '服务器错误，请稍后重试'
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      errorMessage = '无法连接到服务器，请检查网络连接'
    }
    
    addMessage('ai', errorMessage)
  } finally {
    loading.value = false
  }
}

const addMessage = async (sender, content) => {
  messages.value.push({
    sender,
    content,
    timestamp: new Date()
  })
  
  await nextTick()
  scrollToBottom()
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const handleOverlayClick = () => {
  emit('close')
}

// 组件挂载时初始化
onMounted(() => {
  addMessage('ai', `您好！我是ZJU Last1KM的在线客服，很高兴为您服务！请问有什么可以帮助您的吗？

您可以咨询：
• 订单相关问题
• 配送服务问题
• 费用计算问题
• 退款申请
• 其他服务问题`)
})
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.chat-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  padding: 20px;
  box-sizing: border-box;
}

.chat-app {
  width: 100%;
  max-width: 380px;
  height: 80vh;
  max-height: 600px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  margin: 0 auto;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  flex-shrink: 0;
}

.header-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.avatar i {
  font-size: 20px;
  color: white;
}

.service-info h3 {
  margin: 0 0 2px 0;
  font-size: 16px;
  font-weight: 600;
}

.status {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
}

.status.online {
  background-color: #28a745;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
  min-height: 0;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 16px;
  line-height: 1.4;
  position: relative;
  word-wrap: break-word;
  white-space: pre-line;
  font-size: 14px;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.ai {
  align-self: flex-start;
  background-color: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  margin-top: 4px;
  text-align: right;
}

.input-area {
  display: flex;
  padding: 16px;
  background-color: white;
  border-top: 1px solid #e9ecef;
  gap: 10px;
  flex-shrink: 0;
}

.message-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #e9ecef;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
  transition: border-color 0.2s;
  min-width: 0;
}

.message-input:focus {
  border-color: #667eea;
}

.message-input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.send-button {
  padding: 10px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: transform 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 2px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

/* 禁用输入时的样式 */
.input-area.disabled {
  opacity: 0.7;
  pointer-events: none;
}

/* 加载动画样式 */
.glass-loader {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
  border-radius: 14px;
  padding: 14px 16px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.loader-text {
  color: #666;
  font-size: 13px;
  margin-bottom: 10px;
  font-weight: 500;
}

.wave-loader {
  display: flex;
  justify-content: center;
  gap: 4px;
  height: 14px;
}

.wave {
  width: 3px;
  height: 14px;
  background: #667eea;
  border-radius: 2px;
  animation: wave 1.2s ease-in-out infinite;
}

.wave:nth-child(2) { animation-delay: 0.2s }
.wave:nth-child(3) { animation-delay: 0.4s }

@keyframes wave {
  0%, 60%, 100% {
    transform: scaleY(0.4);
    background: rgba(102, 126, 234, 0.6);
  }
  30% {
    transform: scaleY(1);
    background: #667eea;
    box-shadow: 0 0 8px rgba(102, 126, 234, 0.3);
  }
}

/* 响应式设计 */
@media (max-width: 410px) {
  .chat-overlay {
    padding: 10px;
  }
  
  .chat-app {
    height: 85vh;
    border-radius: 15px;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .avatar {
    width: 36px;
    height: 36px;
    margin-right: 10px;
  }
  
  .avatar i {
    font-size: 18px;
  }
  
  .service-info h3 {
    font-size: 15px;
  }
  
  .chat-messages {
    padding: 12px;
    gap: 10px;
  }
  
  .message {
    max-width: 90%;
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .input-area {
    padding: 12px;
    gap: 8px;
  }
  
  .message-input {
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .send-button {
    padding: 8px 14px;
    font-size: 12px;
  }
}

@media (max-width: 350px) {
  .chat-overlay {
    padding: 5px;
  }
  
  .chat-app {
    border-radius: 12px;
  }
  
  .message {
    max-width: 95%;
  }
}
</style>