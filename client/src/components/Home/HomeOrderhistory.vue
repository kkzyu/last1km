// 完全重构此组件以显示真实数据

<template>
  <div class="order-history">
    <div class="section-header">
      <h3>我的历史订单</h3>
      <a-button type="primary" @click="$emit('publish')">
        发布委托
      </a-button>
    </div>

    <div class="order-list" v-if="!orderStore.loading">
      <div v-if="orderStore.orders.length === 0" class="empty-state">
        <a-empty description="暂无订单">
          <a-button type="primary" @click="$emit('publish')">
            发布第一个委托
          </a-button>
        </a-empty>
      </div>
      
      <div v-else>
        <div 
          v-for="order in orderStore.orders" 
          :key="order.id"
          class="order-item"
          @click="viewOrderDetail(order.id)"
        >
          <div class="order-header">
            <div class="order-info">
              <span class="order-id">订单 #{{ order.id }}</span>
              <span :class="['order-status', `status-${order.order_status}`]">
                {{ getStatusText(order.order_status) }}
              </span>
            </div>
            <div class="order-time">
              {{ formatTime(order.created_at) }}
            </div>
          </div>

          <div class="order-content">
            <div class="addresses">
              <div class="address-item">
                <span class="label">起点:</span>
                <span class="value">{{ order.start_address }}</span>
              </div>
              <div class="address-item">
                <span class="label">终点:</span>
                <span class="value">{{ order.end_address }}</span>
              </div>
            </div>

            <div class="order-description" v-if="order.item_description">
              {{ order.item_description }}
            </div>

            <div class="order-footer">
              <div class="amount">
                ¥{{ order.actual_amount.toFixed(2) }}
              </div>
              
              <div class="actions">
                <!-- 待接单状态可以取消 -->
                <a-button 
                  v-if="order.order_status === 'pending'" 
                  size="small" 
                  @click.stop="handleCancel(order.id)"
                >
                  取消
                </a-button>
                
                <!-- 已取消状态可以恢复 -->
                <a-button 
                  v-if="order.order_status === 'cancelled'" 
                  size="small" 
                  type="primary"
                  @click.stop="handleRestore(order.id)"
                >
                  恢复
                </a-button>
                
                <!-- 已完成状态可以评价 -->
                <a-button 
                  v-if="order.order_status === 'completed' && !order.user_rating" 
                  size="small" 
                  type="primary"
                  @click.stop="handleReview(order.id)"
                >
                  评价
                </a-button>

                <!-- 已评价显示评分 -->
                <div v-if="order.user_rating" class="rating">
                  <a-rate :value="order.user_rating" disabled size="small" />
                </div>
              </div>
            </div>
          </div>

          <!-- 配送员信息 (如果已接单) -->
          <div v-if="order.deliverer" class="deliverer-info">
            <span>配送员: {{ order.deliverer.name }}</span>
            <span class="deliverer-phone">{{ order.deliverer.phone }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading">
      <a-spin size="large" />
    </div>

    <!-- 评价对话框 -->
    <a-modal
      v-model:open="reviewModalVisible"
      title="订单评价"
      @ok="submitReview"
      @cancel="closeReviewModal"
    >
      <div class="review-form">
        <div class="form-item">
          <label>评分:</label>
          <a-rate v-model:value="reviewForm.rating" />
        </div>
        <div class="form-item">
          <label>评价:</label>
          <a-textarea 
            v-model:value="reviewForm.comment" 
            placeholder="请输入您的评价..."
            :rows="4"
          />
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOrderStore } from '@/stores/orderStore'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'

// 定义事件
defineEmits(['publish'])

const orderStore = useOrderStore()
const router = useRouter()

// 评价相关状态
const reviewModalVisible = ref(false)
const currentReviewOrderId = ref(null)
const reviewForm = ref({
  rating: 5,
  comment: ''
})

onMounted(() => {
  orderStore.loadOrders()
})

// 状态文本映射
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待接单',
    'accepted': '已接单',
    'delivering': '配送中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 时间格式化
const formatTime = (timeString) => {
  const date = new Date(timeString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理订单操作
const handleCancel = async (orderId) => {
  try {
    await orderStore.cancelOrder(orderId)
    message.success('订单已取消')
  } catch (error) {
    message.error('取消失败')
  }
}

const handleRestore = async (orderId) => {
  try {
    await orderStore.restoreOrder(orderId)
    message.success('订单已恢复')
  } catch (error) {
    message.error('恢复失败')
  }
}

const handleReview = (orderId) => {
  currentReviewOrderId.value = orderId
  reviewModalVisible.value = true
}

const submitReview = async () => {
  try {
    await orderStore.reviewOrder(currentReviewOrderId.value, reviewForm.value)
    message.success('评价成功')
    closeReviewModal()
  } catch (error) {
    message.error('评价失败')
  }
}

const closeReviewModal = () => {
  reviewModalVisible.value = false
  currentReviewOrderId.value = null
  reviewForm.value = { rating: 5, comment: '' }
}

const viewOrderDetail = (orderId) => {
  router.push(`/order/${orderId}`)
}
</script>

<style scoped>
.order-history {
  padding: 16px;
  background: white;
  border-radius: 8px;
  margin: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.order-item {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.order-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-id {
  font-weight: 500;
}

.order-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-pending { background: #fff7e6; color: #fa8c16; }
.status-accepted { background: #e6f7ff; color: #1890ff; }
.status-delivering { background: #f6ffed; color: #52c41a; }
.status-completed { background: #f6ffed; color: #52c41a; }
.status-cancelled { background: #fff2f0; color: #ff4d4f; }

.order-time {
  font-size: 12px;
  color: #666;
}

.addresses {
  margin-bottom: 8px;
}

.address-item {
  margin-bottom: 4px;
  font-size: 14px;
}

.label {
  color: #666;
  margin-right: 8px;
}

.order-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.amount {
  font-weight: 500;
  color: #ff4d4f;
  font-size: 16px;
}

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.deliverer-info {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  font-size: 14px;
  color: #666;
}

.deliverer-phone {
  margin-left: 16px;
}

.review-form .form-item {
  margin-bottom: 16px;
}

.review-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 40px;
}

.empty-state {
  text-align: center;
  padding: 40px;
}
</style>