<template>
  <section class="history-orders">
    <div class="section-header">
      <a-typography-title :level="4" style="margin: 0">我的历史订单</a-typography-title>
      <a-button 
        type="primary" 
        class="publish-button"
        @click="emit('publish')"
      >
        发布委托 +
      </a-button>
    </div>

    <div class="order-list">
      <template 
        v-for="(group, date) in groupedOrders" 
        :key="date"
      >
        <a-card 
          v-for="order in group"
          :key="order.id"
          class="order-item"
          :bordered="true"
          :bodyStyle="{ padding: '15px', display: 'flex', gap: '15px', alignItems: 'flex-start' }"
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
            <a-tag :color="getStatusColor(order.status)" class="order-status">
              {{ order.status }}
            </a-tag>
            <a-typography-paragraph class="order-id">订单号：{{ order.id }}</a-typography-paragraph>
            <a-typography-paragraph>{{ order.from }} → {{ order.to }}</a-typography-paragraph>
            <a-typography-paragraph>速递物品：{{ order.item }}</a-typography-paragraph>
            <a-typography-paragraph v-if="order.eta">
              预计 <a-typography-text type="danger"><strong>{{ order.eta }}</strong></a-typography-text> 分钟后送达
            </a-typography-paragraph>
            <a-typography-paragraph v-else-if="order.description">
              {{ order.description }}
            </a-typography-paragraph>
          </div>

          <div class="order-actions">
            <a-button
              v-if="order.status !== '已完成'"
              danger
              :disabled="order.status !== '进行中'"
              @click="emit('cancel', order.id)"
              size="small"
            >
              取消订单
            </a-button>
            <a-button
              v-if="order.status === '已完成'"
              type="primary"
              @click="emit('review', order.id)"
              size="small"
            >
              评价订单
            </a-button>
            <a-button
              v-if="order.status === '已取消'"
              type="primary"
              style="background-color: #4CAF50; border-color: #4CAF50;" 
              @click="emit('restore', order.id)"
              size="small"
            >
              恢复订单
            </a-button>
          </div>
        </a-card>
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useOrderStore } from '@/stores/orderStore';

// 使用Pinia store
const orderStore = useOrderStore();
const groupedOrders = computed(() => orderStore.groupedOrders);

const emit = defineEmits(['publish', 'cancel', 'review', 'restore', 'image-error']);
const BASE_URL = import.meta.env.BASE_URL;

const getImageUrl = (imagePath) => {
  if (!imagePath || typeof imagePath !== 'string') {
    return '';
  }

  if (BASE_URL === '/') {
    return imagePath;
  }

  const cleanBase = BASE_URL.endsWith('/') ? BASE_URL.slice(0, -1) : BASE_URL;
  return `${cleanBase}${imagePath}`;
}

// 获取状态对应的颜色
const getStatusColor = (status) => {
  switch(status) {
    case '进行中': return 'processing';
    case '已完成': return 'success';
    case '已取消': return 'error';
    default: return 'default';
  }
}

// 图片错误处理函数
const handleImageError = (orderId) => {
  console.error('图片加载失败:', orderId);
  emit('image-error', orderId);
}
</script>

<style scoped>
.history-orders {
  padding: 15px;
  flex: 1;
  overflow-y: auto; 
  height: 0;  
  padding-bottom: 55px;
  background-color: #fff; /* 内容区域使用白色背景 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.publish-button {
  border-radius: 20px; /* 保持胶囊形状 */
  font-size: 1em;
  /* Ant Design primary button 会自动使用主题色, 无需额外颜色设置 */
}

.order-list .order-item {
  margin-bottom: 15px;
  border-radius: 10px; /* 统一圆角为 10px */
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* 统一阴影 */
}

.order-list .order-item:last-child {
  margin-bottom: 25px;
}

.order-image {
  width: 100px;
  height: 120px;
  border-radius: 8px; /* 图片容器圆角 */
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
  left: 0%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 0.9em;
}

.order-details {
  flex: 1;
  min-width: 0;
}

.order-status {
  margin-bottom: 8px;
  letter-spacing: 0.5px;
  display: inline-block;
}

:deep(.ant-typography) {
  font-size: 0.9em;
  color: #333; /* 常规文字颜色 */
  margin: 5px 0;
  line-height: 1.4;
  letter-spacing: 0.3px;
  /* 移除了 font-family, 使用 Ant Design 默认或全局字体 */
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.order-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;  
  margin-left: auto;
  width: 65px; /* 根据按钮实际宽度可能需要微调 */
}

/* 确保按钮大小和间距适合小空间 */
.order-actions .ant-btn-sm {
  padding-left: 0;
  padding-right: 0;
  width: 100%; /* 让按钮宽度一致 */
  text-align: center;
}


/* 响应式设计 */
@media (max-width: 768px) {
  /* :deep(.ant-typography) 已经设置了文本溢出处理, 这里可能无需重复 */
}
</style>