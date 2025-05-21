<template>
  <section class="history-orders">
    <div class="section-header">
      <h2>我的历史订单</h2>
      <button 
        class="publish-button"
        @click="emit('publish')"
      >
        发布委托 +
      </button>
    </div>

    <div class="order-list">
      <template 
        v-for="(group, date) in groupedOrders" 
        :key="date"
      >
        <div
          v-for="order in group"
          :key="order.id"
          :class="{
            'order-item': true,
            'in-progress': order.status === '进行中',
            'cancelled': order.status === '已取消',
            'completed': order.status === '已完成'
          }"
        >
          <div class="order-image">
            <img 
              :src="getImageUrl(order.image)" 
              alt="订单图片"
              @error="handleImageError(order.id)"
            >
            <div v-if="!order.image" class="image-placeholder">暂无图片</div>
          </div>

          <div class="order-details">
            <div class="order-status">{{ order.status }}</div>
            <p class="order-id">订单号：{{ order.id }}</p>
            <p>{{ order.from }} → {{ order.to }}</p>
            <p>速递物品：{{ order.item }}</p>
            <p v-if="order.eta">
              预计 <span>{{ order.eta }}</span> 分钟后送达
            </p>
            <p v-else-if="order.description">
              {{ order.description }}
            </p>
          </div>

          <div class="order-actions">
            <button
              v-if="order.status !== '已完成'"
              class="cancel-button"
              :disabled="order.status !== '进行中'"
              @click="emit('cancel', order.id)"
            >
              取消订单
            </button>
            <button
              v-if="order.status === '已完成'"
              class="review-button"
              @click="emit('review', order.id)"
            >
              评价订单
            </button>
            <div class="order-actions">
              <button
                v-if="order.status === '已取消'"
                class="restore-button"
                @click="emit('restore', order.id)"
              >
                恢复订单
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

defineProps({
  groupedOrders: {
    type: Object,
    required: true
  }
})


const emit = defineEmits(['publish', 'cancel', 'review', 'restore', 'image-error'])


const getImageUrl = (imagePath) => {
  if (!imagePath) {
    return '' // Return empty string if no path is provided
  }
  return imagePath
}

// 添加图片错误处理函数
const handleImageError = (orderId) => {
  console.error('图片加载失败:', orderId)
  emit('image-error', orderId)
}
</script>

<style scoped>
/* 历史订单区域 */
.history-orders {
  padding: 15px;
  flex: 1;
  overflow-y: auto; 
  height: 0;  
  padding-bottom: 55px;
  background-color: #fff;
}

.order-list .order-item {
  background-color: #eee; 
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 15px;
  align-items: flex-start;
  justify-content: space-between;
  border: 1px solid #ddd; 
}

.order-list .order-item:last-child {
  margin-bottom: 25px;
}

.history-orders .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.history-orders h2 {
  font-size: 1.2em;
  color: #333;
  margin: 0;
}

.history-orders .publish-button {
  background-color: #1976D2;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1em;
}

/* 订单列表项样式 */
.order-list .order-item {
  background-color: white;
  border-radius: 15px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 15px;
  align-items: flex-start;
  justify-content: space-between;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.order-item .order-status {
  font-weight: 600;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif; /* 更优雅的字体 */
}

.order-item p {
  font-size: 0.9em;
  color: #333;
  margin: 5px 0;
  line-height: 1.4; /* 增加行高提升可读性 */
  letter-spacing: 0.3px;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif; /* 统一字体 */
  font-weight: 400; /* 标准字重 */
}

.order-item p span {
  color: #E91E63;
  font-weight: 600; /* 加粗强调 */
  font-family: inherit; /* 继承父元素字体 */
}

.order-details {
  flex: 1;
  min-width: 0; 
}

.order-item p {
  font-size: 0.9em;
  color: #333;
  margin: 5px 0;
  line-height: 1.2;
  letter-spacing: 0.3px;
  white-space: nowrap;
  overflow: hidden;      /* 确保生效 */
  text-overflow: ellipsis; /* 确保生效 */
  max-width: 100%;       /* 新增 */
}

.order-item p span {
  color: #E91E63;
  font-weight: bold;
}

/* 按钮样式 */
.order-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;  
  margin-left: auto;
  width: 65px;  
}

.order-item .review-button,
.order-item .cancel-button {
  width: 100%;
  border: none;
  padding: 5px;  
  border-radius: 6px;  
  cursor: pointer;
  font-size: 0.8em;  
  text-align: center;
  white-space: nowrap;
  font-weight: 600;  
  min-height: 28px; 
}

.order-item .cancel-button {
  background-color: #f44336;
  color: white;
}

.order-item .cancel-button:disabled {
  background-color: #bdbdbd;
  cursor: not-allowed;
}

.order-item .review-button {
  background-color: #2196F3;
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-orders h2 {
    font-size: 1.1em;
  }
  
  .history-orders .publish-button {
    padding: 8px 12px;
    font-size: 0.9em;
  }
  
  .order-item p {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.order-image {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
  background: #f5f5f5;
}

.order-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 0.9em;
}

.order-item .restore-button {
  background-color: #4CAF50;
  color: white;
  width: 100%;
  border: none;
  padding: 5px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8em;
  text-align: center;
  white-space: nowrap;
  font-weight: 600;
  min-height: 28px;
}

</style>