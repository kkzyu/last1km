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
              <a-typography-text type="secondary" class="order-no">
                订单号: {{ order.order_no || '无' }}
              </a-typography-text>
              <div> 
                <a-typography-text class="order-route">{{ transformOrder(order).origin }} → {{ transformOrder(order).destination }} </a-typography-text>
              </div>
              <div>
                <a-typography-text type="secondary" class="order-item-description">
                  委托物品：{{ transformOrder(order).description || '无描述' }}
                </a-typography-text>
              </div>
            </div>
            <div class="order-actions">
              <a-button
                v-if="transformOrder(order).status === 'pending'"
                type="primary" 
                ghost
                size="small"
                @click="emit('cancel', order.id)"
              >
                取消
              </a-button>
              <a-button
                v-else-if="transformOrder(order).status === 'completed'"
                type="primary"
                size="small"
                @click="emit('review', order.id)"
              >
                评价
              </a-button>
              <a-button
                v-else-if="transformOrder(order).status === 'cancelled'"
                type="primary"
                danger
                ghost
                size="small"
                @click="emit('delete', order.id)"
              >
                删除
              </a-button>
            </div>
          </a-card>
        </div>
      </template>
      <div v-if="!Object.keys(groupedOrders).length && !orderStore.isLoading" class="empty-state">
        <a-empty description="暂无符合条件的订单" />
      </div>
       <div v-if="orderStore.isLoading" class="loading-state" style="text-align: center; padding: 20px;">
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
const router = useRouter();  // 已经在这里声明过了
const groupedOrders = computed(() => orderStore.groupedOrders);
const imageFailedStates = ref({});

const emit = defineEmits(['publish', 'cancel', 'review', 'delete']);

// 定义API基础URL，用于拼接图片路径 (与RequestDetailsForm.vue中保持一致)
const API_BASE_URL = 'http://localhost:5000'; 

onMounted(() => {
  orderStore.loadOrders();
});

const getImageUrl = (imageFilename) => { // 参数名改为 imageFilename 更清晰
  if (!imageFilename) return '';
  // 假设 imageFilename 是后端存储的文件名，例如 "your-uuid.png"
  return `${API_BASE_URL}/static/uploads/${imageFilename}`; 
}

const transformOrder = (order) => {
  return {
    ...order,
    origin: order.start_address,
    destination: order.end_address,
    image: order.order_image, // order.order_image 应该存储的是文件名
    amount: order.actual_amount,
    status: order.order_status,
    description: order.item_description
  }
}

const getDisplayStatus = (status) => {
  switch(status) {
    case 'pending': return '进行中';
    case 'completed': return '已完成';
    case 'cancelled': return '已取消';
    default: return status ? status.charAt(0).toUpperCase() + status.slice(1) : '未知';
  }
}

const getStatusColor = (status) => {
  switch(status) {
    case 'pending': return 'processing';
    case 'completed': return 'success';
    case 'cancelled': return 'error';
    default: return 'default';
  }
}

const handleImageError = (orderId) => {
  imageFailedStates.value[orderId] = true;
}

// 删除下面重复的 router 声明
// const router = useRouter();

const handleOrderClick = (orderId) => {
  router.push(`/orders/${orderId}`);
};
</script>

<style scoped>
.history-orders {
  padding: 15px;
  flex: 1;
  height: 0;
  padding-bottom: 55px;
  background-color: #f5f5f7; /* 外层容器设置为浅灰色 */
}

.order-list {
  background-color: #f5f5f7; 
  border-radius: 8px; /* 添加圆角 */
  padding: 10px; /* 添加内边距 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.publish-button {
  border-radius: 20px;
  font-size: 1em;
}

.order-list .order-item { /* 这是 a-card 的样式 */
  margin-bottom: 15px;
  border-radius: 10px;
  overflow: hidden; /* 有助于内部圆角和阴影的显示 */
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  /* a-card 的 :bodyStyle 已经设置了 display:flex, gap, alignItems */
}

.order-list .order-item:last-child {
  margin-bottom: 25px;
}

.order-image {
  width: 80px; /* 根据需要调整图片宽度 */
  height: 80px; /* 根据需要调整图片高度 */
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0; /* 防止图片在flex布局中被压缩 */
  background: #f0f0f0; /* 图片加载前的占位背景色 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.order-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例并填充容器 */
}

.image-placeholder {
  color: #999;
  font-size: 2em; /* 调整占位图标大小 */
}

.order-details {
  flex-grow: 1;   /* 占据剩余空间 */
  flex-shrink: 1; /* 允许收缩 */
  min-width: 0;     /* **非常重要**：允许flex项收缩到其内容大小以下，以便max-width和省略号生效 */
  max-width: 200px; /* 您要求的最大宽度，可以调整这个值，例如 '50%' 或其他像素值 */
  overflow: hidden; /* 隐藏超出最大宽度的内容，配合文本省略 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直方向上内容居中（如果需要） */
}

.order-status {
  margin-bottom: 4px;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
  display: inline-block; /* 或者 flex-start 如果想让它不占满整行 */
  align-self: flex-start; /* 确保标签靠左 */
}

.order-no {
  display: block;
  font-size: 12px; /* 保持与状态标签字体大小一致或略小 */
  color: #999;
  white-space: nowrap; /* 确保订单号本身如果过长也会省略 */
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%; /* 相对于.order-details的宽度 */
  /* margin-bottom: 6px; /* 从order-details内部的文本中移除，因为外部有gap */
}

/* 针对订单详情中的文本行应用省略号 */
.order-details .order-route,
.order-details .order-item-description {
  display: block; 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%; 
  font-size: 14px;
  line-height: 1.5;
}
.order-details .order-route {
 color: #333; /* 主要文本颜色 */
 margin: 2px 0; /* 调整间距 */
}

.order-details .order-item-description {
  color: #555; 
  font-size: 13px; 
  margin-top: 2px; /* 调整间距 */
}


.date-header {
  padding: 10px 0;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.order-actions {
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center; 
  gap: 8px;
  flex-shrink: 0; 
  padding-left: 10px; 
  width: 70px; 
}

.order-actions .ant-btn {
  width: 100%;
  text-align: center;
}

.date-group {
  margin-bottom: 20px;
}

.empty-state, .loading-state {
  padding: 40px 0;
  text-align: center;
}
</style>