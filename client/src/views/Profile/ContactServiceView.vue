<template>
  <div class="contact-service-container">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h1 class="title">联系客服</h1>
    </div>
    
    <div class="content">
      <div class="welcome-section">
        <div class="service-icon">
          <i class="fas fa-headphones"></i>
        </div>
        <h2>欢迎联系我们的客服团队</h2>
        <p>我们的客服团队随时为您提供帮助</p>
      </div>

      <div class="contact-methods">
        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-phone"></i>
          </div>
          <div class="contact-info">
            <h3>客服热线</h3>
            <p>400-123-4567</p>
            <span class="service-time">工作日 9:00-18:00</span>
          </div>
        </div>

        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-envelope"></i>
          </div>
          <div class="contact-info">
            <h3>邮箱咨询</h3>
            <p>service@zjulast1km.com</p>
            <span class="service-time">24小时内回复</span>
          </div>
        </div>

        <div class="contact-item">
          <div class="contact-icon">
            <i class="fas fa-comments"></i>
          </div>
          <div class="contact-info">
            <h3>在线客服</h3>
            <p>点击开始对话</p>
            <span class="service-time">服务时间: 24小时</span>
          </div>
          <button class="chat-button" @click="startChat">
            <i class="fas fa-comment-dots"></i>
            开始对话
          </button>
        </div>
      </div>

      <div class="faq-section">
        <div class="faq-header">
          <h3>常见问题</h3>
          <button v-if="!showAllFaq && faqList.length > 3" 
                  class="show-more-btn" 
                  @click="toggleFaqDisplay">
            查看更多
          </button>
          <button v-if="showAllFaq" 
                  class="show-more-btn" 
                  @click="toggleFaqDisplay">
            收起
          </button>
        </div>
        
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="error" class="error-container">
          <p>{{ error }}</p>
          <button class="retry-btn" @click="fetchFaqData">重试</button>
        </div>
        
        <div v-else>
          <div v-for="faq in displayedFaqList" 
               :key="faq.id" 
               class="faq-item"
               @click="toggleFaqItem(faq.id)">
            <div class="faq-question">
              <p><strong>Q: {{ faq.question }}</strong></p>
              <i class="fas fa-chevron-down" 
                 :class="{ 'rotated': expandedItems.includes(faq.id) }"></i>
            </div>
            <div v-show="expandedItems.includes(faq.id)" class="faq-answer">
              <p>A: {{ faq.answer }}</p>
              <span v-if="faq.category" class="faq-category">分类：{{ faq.category }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加客服聊天弹窗 -->
    <CustomerChat 
      v-if="showChat" 
      @close="closeChat" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import CustomerChat from '@/components/Profile/CustomerChat.vue'

const router = useRouter()

// 响应式数据
const faqList = ref([])
const loading = ref(false)
const error = ref('')
const showAllFaq = ref(false)
const expandedItems = ref([])

// 新增聊天相关状态
const showChat = ref(false)

// 计算属性：显示的FAQ列表
const displayedFaqList = computed(() => {
  if (showAllFaq.value) {
    return faqList.value
  }
  return faqList.value.slice(0, 3)
})

// 方法：获取FAQ数据
const fetchFaqData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.get('/api/faq/list')
    
    if (response.data.success) {
      faqList.value = response.data.data || []
      // 默认展开第一个FAQ项
      if (faqList.value.length > 0) {
        expandedItems.value = [faqList.value[0].id]
      }
    } else {
      error.value = response.data.message || '获取FAQ数据失败'
    }
  } catch (err) {
    console.error('获取FAQ数据失败:', err)
    error.value = '网络错误，请检查网络连接'
    
    // 使用备用数据 - 修复引号问题
    faqList.value = [
      {
        id: 1,
        question: "如何取消订单？",
        answer: "在订单详情页面点击'取消订单'按钮即可。",
        category: "订单管理"
      },
      {
        id: 2,
        question: "配送费如何计算？",
        answer: "配送费根据距离和时间段动态计算。",
        category: "费用说明"
      },
      {
        id: 3,
        question: "如何申请退款？",
        answer: "请联系客服或在订单页面申请退款。",
        category: "退款政策"
      }
    ]
  } finally {
    loading.value = false
  }
}

// 方法：切换FAQ显示数量
const toggleFaqDisplay = () => {
  showAllFaq.value = !showAllFaq.value
}

// 方法：切换FAQ项展开/收起
const toggleFaqItem = (faqId) => {
  const index = expandedItems.value.indexOf(faqId)
  if (index > -1) {
    expandedItems.value.splice(index, 1)
  } else {
    expandedItems.value.push(faqId)
  }
}

// 方法：开始聊天
const startChat = () => {
  showChat.value = true
}

// 方法：关闭聊天
const closeChat = () => {
  showChat.value = false
}

// 生命周期：组件挂载时获取数据
onMounted(() => {
  fetchFaqData()
})
</script>

<style scoped>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css");

.contact-service-container {
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  max-height: 100vh;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.contact-service-container::-webkit-scrollbar {
  display: none;
}

.header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-button {
  background: none;
  border: none;
  font-size: 18px;
  color: #333;
  cursor: pointer;
  padding: 8px;
  margin-right: 15px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.content {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: 40px 20px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.service-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.service-icon i {
  font-size: 36px;
  color: white;
}

.welcome-section h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 600;
}

.welcome-section p {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.contact-methods {
  margin-bottom: 30px;
}

.contact-item {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.contact-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.contact-icon {
  width: 50px;
  height: 50px;
  background-color: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.contact-icon i {
  font-size: 20px;
  color: #667eea;
}

.contact-info {
  flex: 1;
}

.contact-info h3 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.contact-info p {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.service-time {
  color: #999;
  font-size: 12px;
}

.chat-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  padding: 12px 20px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.chat-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.chat-button i {
  margin-right: 8px;
}

.faq-section {
  background-color: #ffffff;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.faq-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.show-more-btn {
  background: none;
  border: 1px solid #667eea;
  color: #667eea;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.show-more-btn:hover {
  background-color: #667eea;
  color: white;
}

.loading-container {
  text-align: center;
  padding: 40px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 20px;
  color: #e74c3c;
}

.retry-btn {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  margin-top: 10px;
}

.faq-item {
  margin-bottom: 15px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
  cursor: pointer;
}

.faq-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
}

.faq-question p {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.faq-question i {
  color: #667eea;
  transition: transform 0.2s;
}

.faq-question i.rotated {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #f0f0f0;
}

.faq-answer p {
  margin: 0 0 10px 0;
  color: #666;
  line-height: 1.5;
}

.faq-category {
  display: inline-block;
  background-color: #667eea;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 500;
}
</style>