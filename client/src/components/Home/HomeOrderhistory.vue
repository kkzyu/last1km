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
            @click="router.push(`/orders/${order.id}`)"
          >
            <div class="order-image">
              <img 
                v-if="transformOrder(order).image && !imageFailedStates[order.id]" 
                :src="getImageUrl(transformOrder(order).image)"
                @error="() => handleImageError(order.id)"
                alt="订单图片"
              />
              <div v-else class="image-placeholder">
                <picture-outlined />
              </div>
            </div>
            <div class="order-details">
              <a-tag :color="getStatusColor(transformOrder(order).status)" class="order-status">
                {{ getDisplayStatus(transformOrder(order).status) }}
              </a-tag>
              <div v-if="transformOrder(order).estimatedTime" class="delivery-info">
                <a-typography-text type="secondary" class="delivery-time">
                  🚴‍♂️ 预计{{ transformOrder(order).estimatedTime.duration }}分钟 · {{ transformOrder(order).estimatedTime.distance }}km
                </a-typography-text>
              </div>
              
              <div>
                <a-typography-text type="secondary" class="order-item-description">
                  委托物品：{{ transformOrder(order).description || '无描述' }}
                </a-typography-text>
              </div>
              
              <!-- 显示金额信息 -->
              <div class="order-amount">
                <a-typography-text class="amount-text">
                  委托金额：¥{{ transformOrder(order).amount?.toFixed(2) || '0.00' }}
                </a-typography-text>
              </div>
            </div>
            <div class="order-actions">
              <a-button
                v-if="transformOrder(order).status === 'pending'"
                type="primary" 
                ghost
                size="small"
                @click.stop="emit('cancel', order.id)"
              >
                取消
              </a-button>
              <a-button
                v-else-if="transformOrder(order).status === 'completed'"
                type="primary"
                size="small"
                @click.stop="emit('review', order.id)"
              >
                评价
              </a-button>
              <a-button
                v-else-if="transformOrder(order).status === 'cancelled'"
                type="primary"
                danger
                ghost
                size="small"
                @click.stop="emit('delete', order.id)"
              >
                删除
              </a-button>
            </div>
          </a-card>
        </div>
      </template>
      <div v-if="!hasOrders && !orderStore.loading" class="empty-state">
        <a-empty description="暂无符合条件的订单" />
      </div>
      
      <div v-if="orderStore.loading" class="loading-state" style="text-align: center; padding: 20px;">
        <a-spin size="large" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/orderStore';
import { PictureOutlined } from '@ant-design/icons-vue';

const orderStore = useOrderStore();
const router = useRouter();
const groupedOrders = computed(() => orderStore.groupedOrders);
const imageFailedStates = ref({});

const emit = defineEmits(['publish', 'cancel', 'review', 'delete']);

const API_BASE_URL = 'http://localhost:5000'; 

const safeGroupedOrders = computed(() => {
  const orders = orderStore.groupedOrders;
  return orders && typeof orders === 'object' ? orders : {};
});

const hasOrders = computed(() => {
  const orders = safeGroupedOrders.value;
  return orders && Object.keys(orders).length > 0;
});


onMounted(async () => {
  // 修改为使用正确的方法名
  try {
    if (typeof orderStore.fetchOrders === 'function') {
      await orderStore.fetchOrders();
    } else if (typeof orderStore.loadOrders === 'function') {
      await orderStore.loadOrders();
    } else {
      console.warn('orderStore 中没有找到加载订单的方法');
    }
  } catch (error) {
    console.error('加载订单失败:', error);
  }
});


const getImageUrl = (imageFilename) => {
  if (!imageFilename) return '';
  return `${API_BASE_URL}/static/uploads/${imageFilename}`; 
}

const transformOrder = (order) => {
  // 解析预计配送时间
  let estimatedTime = null;
  if (order.estimated_duration && order.estimated_distance) {
    estimatedTime = {
      duration: order.estimated_duration,
      distance: order.estimated_distance,
      mode: '骑行'
    };
  }

  return {
    ...order,
    origin: order.origin || order.start_address || '未知起点',
    destination: order.destination || order.end_address || '未知终点',
    originDetail: order.origin_detail || '',
    destinationDetail: order.destination_detail || '',
    image: order.order_image,
    amount: order.actual_amount || order.amount || order.total_amount,
    status: order.order_status || order.status,
    description: order.item_description || order.description,
    estimatedTime
  }
}

const getDisplayStatus = (status) => {
  switch(status) {
    case 'pending': return '进行中';
    case 'accepted': return '已接单';
    case 'delivering': return '配送中';
    case 'completed': return '已完成';
    case 'cancelled': return '已取消';
    case 'reviewed': return '已评价';
    default: return status ? status.charAt(0).toUpperCase() + status.slice(1) : '未知';
  }
}

const getStatusColor = (status) => {
  switch(status) {
    case 'pending': return 'processing';
    case 'accepted': return 'blue';
    case 'delivering': return 'orange';
    case 'completed': return 'success';
    case 'cancelled': return 'error';
    case 'reviewed': return 'purple';
    default: return 'default';
  }
}

const handleImageError = (orderId) => {
  imageFailedStates.value[orderId] = true;
}

const handleOrderClick = (orderId) => {
  router.push(`/orders/${orderId}`);
};
</script>

<style scoped>
.history-orders {
  padding: 16px;
  background-color: var(--color-bg-container);
  min-height: 100%;
  max-height: calc(100vh - 80px); /* 设置最大高度，减去头部和底部导航的高度 */
  overflow-y: auto; /* 启用垂直滚动 */
  box-sizing: border-box;
  /* 隐藏滚动条 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}

/* 隐藏 Webkit 浏览器的滚动条 */
.history-orders::-webkit-scrollbar {
  display: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.publish-button {
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.order-list {
  background-color: var(--color-bg-container);
  border-radius: 8px;
  max-height: calc(100vh - 20px); /* 为订单列表设置最大高度 */
  overflow-y: auto; /* 启用垂直滚动 */
  /* 隐藏滚动条 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}

/* 隐藏 Webkit 浏览器的滚动条 */
.order-list::-webkit-scrollbar {
  display: none;
}

.date-group {
  margin-bottom: 24px;
}

.date-header {
  padding: 12px 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  position: sticky;
  top: 0;
  background-color: var(--color-bg-container);
  z-index: 1;
}

.order-item {
  margin-bottom: 12px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--box-shadow-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--color-border-secondary);
}

.order-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--box-shadow);
  border-color: var(--color-primary);
}

.order-image {
  width: 80px;
  height:150px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-fill-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.order-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  color: var(--color-text-placeholder);
  font-size: 24px;
}

.order-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.order-status {
  font-size: 12px;
  font-weight: 500;
  align-self: flex-start;
  margin: 0;
}

.order-no {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.route-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 4px 0;
}

.route-point {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.point-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
  margin-top: 2px;
}

.point-icon.start {
  background-color: var(--color-success);
}

.point-icon.end {
  background-color: var(--color-primary);
}

.main-address {
  color: var(--color-text);
  font-size: 13px;
  font-weight: 500;
}

.detail-address {
  color: var(--color-text-tertiary);
  font-size: 12px;
  margin-top: 2px;
}

.delivery-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-primary);
}

.order-item-description {
  color: var(--color-text-secondary);
  font-size: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2; /* 标准属性 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.order-amount {
  margin-top: auto;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-error);
}

.order-actions {
  display: flex;
  align-items: center;
}

.empty-state, 
.loading-state {
  padding: 40px 0;
  text-align: center;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-item {
    flex-direction: column;
  }
  
  .order-image {
    width: 100%;
    height: 120px;
    margin-bottom: 12px;
  }
  
  .order-actions {
    align-self: flex-end;
    margin-top: 12px;
  }

  .history-orders {
    max-height: calc(100vh - 140px); /* 在移动端调整最大高度 */
  }

  .order-list {
    max-height: calc(100vh - 220px); /* 在移动端调整订单列表最大高度 */
  }
}
</style>