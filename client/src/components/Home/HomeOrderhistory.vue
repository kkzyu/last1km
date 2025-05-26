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
        <div class="date-group">
          <div class="date-header">{{ date }}</div>
          <a-card 
            v-for="order in group"
            :key="order.id"
            class="order-item"
            :bodyStyle="{ padding: '15px', display: 'flex', gap: '15px', alignItems: 'flex-start' }"
          >
            <div class="order-image">
              <img 
                v-if="order.image && !imageFailed" 
                :src="getImageUrl(order.image)"
                @error="handleImageError"
                alt="订单图片"
              />
              <div v-else class="image-placeholder">
                <a-icon type="picture" />
              </div>
            </div>
            <div class="order-details">
              <a-tag :color="getStatusColor(order.status)" class="order-status">
                {{ order.status }}
              </a-tag>
              <a-typography-text>从: {{ order.origin }}</a-typography-text>
              <br>
              <a-typography-text>到: {{ order.destination }}</a-typography-text>
              <br>
              <a-typography-text type="secondary">
                {{ order.description || '无描述' }}
              </a-typography-text>
            </div>
            <div class="order-actions">
              <a-typography-text type="danger">￥{{ order.amount }}</a-typography-text>
              <a-button 
                v-if="order.status === '待接单'"
                type="text"
                size="small"
                @click="emit('cancel', order.id)"
              >
                取消
              </a-button>
            </div>
          </a-card>
        </div>
      </template>
      <div v-if="!Object.keys(groupedOrders).length" class="empty-state">
        <a-empty description="暂无订单" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useOrderStore } from '@/stores/orderStore';

const orderStore = useOrderStore();
const groupedOrders = computed(() => orderStore.groupedOrders);
const imageFailed = computed(() => orderStore.imageFailed);

const emit = defineEmits(['publish', 'cancel', 'image-error']);

onMounted(() => {
  orderStore.loadOrders();
});

const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  return `/api/static/uploads/${imagePath}`;
}

const getStatusColor = (status) => {
  switch(status) {
    case '进行中': return 'processing';
    case '配送中': return 'warning';
    case '已完成': return 'success';
    case '已取消': return 'error';
    case '待接单': return 'default';
    default: return 'default';
  }
}

const handleImageError = () => {
  orderStore.handleImageError();
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

.date-group {
  margin-bottom: 20px;
}

.date-header {
  padding: 10px 0;
  color: #666;
  font-size: 0.9em;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  /* :deep(.ant-typography) 已经设置了文本溢出处理, 这里可能无需重复 */
}
</style>