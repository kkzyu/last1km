<template>
  <div class="order-detail-container">
    <OrderDetailHeader />
    <div class="scrollable-content">
      <div v-if="isLoading" class="loading-spinner">
        <a-spin size="large" />
      </div>

      <div v-else-if="order && order.id" class="order-content">
        <a-card :bordered="false" class="order-card">
          <div class="order-meta">
            <a-tag :color="getStatusColor(order.order_status)" class="status-tag">
              {{ getDisplayStatus(order.order_status) }}
            </a-tag>
            <div class="order-no">订单号: {{ order.order_no }}</div>
            <div class="order-time">创建时间: {{ formatDate(order.created_at) }}</div>
            <div v-if="order.cancelled_at" class="order-time">取消时间: {{ formatDate(order.cancelled_at) }}</div>
            <div v-if="order.completed_at" class="order-time">完成时间: {{ formatDate(order.completed_at) }}</div>
          </div>

          <!-- 更新路线信息显示 -->
        <div class="order-route">
          <div class="route-point start">
            <div class="point-icon">起</div>
            <div class="point-detail">
              <div class="main-address">{{ order.start_address }}</div>
              <div v-if="order.origin_detail" class="detail-address">
                具体位置：{{ order.origin_detail }}
              </div>
            </div>
          </div>
          <div class="route-line"></div>
          <div class="route-point end">
            <div class="point-icon">终</div>
            <div class="point-detail">
              <div class="main-address">{{ order.end_address }}</div>
              <div v-if="order.destination_detail" class="detail-address">
                具体位置：{{ order.destination_detail }}
              </div>
            </div>
          </div>
        </div>

          <!-- 显示预计配送信息 -->
          <div v-if="order.estimated_duration || order.estimated_distance" class="delivery-estimate">
            <h3 class="section-title">配送预估</h3>
            <div class="estimate-info">
              <div v-if="order.estimated_duration" class="estimate-item">
                <span class="label">预计时长:</span>
                <span class="value">{{ order.estimated_duration }} 分钟</span>
              </div>
              <div v-if="order.estimated_distance" class="estimate-item">
                <span class="label">预计距离:</span>
                <span class="value">{{ order.estimated_distance }} 公里</span>
              </div>
              <div class="estimate-item">
                <span class="label">配送方式:</span>
                <span class="value">🚴‍♂️ 骑行</span>
              </div>
            </div>
          </div>

          <div class="order-image-section" v-if="order.order_image">
            <h3 class="section-title">订单图片</h3>
            <a-image
              :width="150"
              :src="getImageUrl(order.order_image)"
              :preview="{ visible: previewVisible, onVisibleChange: setPreviewVisible, src: getImageUrl(order.order_image) }"
              class="order-image-preview"
              alt="订单图片"
            />
          </div>
          
          <a-divider />

          <div class="order-info">
            <h3 class="section-title">订单信息</h3>
            <div class="info-item">
              <span class="label">物品描述:</span>
              <span class="value">{{ order.item_description || '无' }}</span>
            </div>
            <div class="info-item" v-if="order.pickup_code">
              <span class="label">取件信息:</span>
              <span class="value">{{ order.pickup_code }}</span>
            </div>
            
          </div>

          <a-divider />

          <div class="order-amount">
            <h3 class="section-title">金额明细</h3>
            <div class="amount-item">
              <span>订单金额:</span>
              <span class="amount">¥{{ (order.total_amount || order.amount || 0).toFixed(2) }}</span>
            </div>
            <div class="amount-item" v-if="order.coupon_discount != null && order.coupon_discount > 0">
              <span>优惠券减免:</span>
              <span class="discount">-¥{{ order.coupon_discount.toFixed(2) }}</span>
            </div>
            <div class="amount-item total">
              <span>实付金额:</span>
              <span class="total-amount">¥{{ (order.actual_amount || order.amount || 0).toFixed(2) }}</span>
            </div>
          </div>
        </a-card>

        <a-card v-if="order.deliverer" title="配送员信息" class="deliverer-card section-card">
          <div class="deliverer-info">
            <a-avatar :src="getImageUrl(order.deliverer.avatar, true)" size="large" v-if="order.deliverer.avatar" />
            <a-avatar size="large" v-else><template #icon><UserOutlined /></template></a-avatar>
            <div class="deliverer-detail">
              <div class="name">{{ order.deliverer.name || '匿名配送员' }}</div>
              <div class="rating" v-if="order.deliverer.rating != null">
                <a-rate :value="order.deliverer.rating" disabled allow-half />
                <span class="rating-text">{{ order.deliverer.rating.toFixed(1) }}</span>
              </div>
            </div>
          </div>
        </a-card>

        <div class="action-buttons">
          <a-button
            v-if="order.order_status === 'pending'"
            type="primary"
            block
            @click="handleCompleteOrder"
          >
            已收到
          </a-button>
          <a-button
            v-if="order.order_status === 'pending'"
            type="primary"
            danger
            block
            @click="handleCancelOrder"
          >
            取消订单
          </a-button>
          <a-button
            v-if="order.order_status === 'completed' && !order.user_review" 
            type="primary"
            block
            @click="handleReviewOrder"
          >
            评价订单
          </a-button>
          <a-button
            v-if="order.order_status === 'cancelled'"
            type="default" 
            danger
            block
            @click="handleDeleteOrder"
          >
            删除订单
          </a-button>
        </div>
      </div>
      <div v-else-if="!isLoading && (!order || !order.id)" class="empty-state">
          <a-empty description="未找到订单信息或加载失败" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { orderAPI } from '@/api/api';
import { message, Image as AImage, Rate as ARate, Avatar as AAvatar, Spin as ASpin } from 'ant-design-vue';
import { UserOutlined } from '@ant-design/icons-vue';
import OrderDetailHeader from '@/components/Header/OrderDetailHeader.vue';

const route = useRoute();
const router = useRouter();
const order = ref(null);
const isLoading = ref(true);
const previewVisible = ref(false);

const API_BASE_URL = 'http://localhost:5000';

const getImageUrl = (imagePath, isFullPathOrAvatar = false) => {
  if (!imagePath) return '';
  if (isFullPathOrAvatar && (imagePath.startsWith('http') || imagePath.startsWith('/'))) {
    return imagePath; 
  }
  return `${API_BASE_URL}/static/uploads/${imagePath}`;
};

const getDisplayStatus = (status) => {
  const statusMap = {
    pending: '进行中',
    accepted: '已接单',
    delivering: '配送中',
    completed: '已完成',
    cancelled: '已取消',
    reviewed: '已评价'
  };
  return statusMap[status] || status;
};

const getStatusColor = (status) => {
  const colorMap = {
    pending: 'processing',
    accepted: 'blue',
    delivering: 'orange',
    completed: 'success',
    cancelled: 'error',
    reviewed: 'purple'
  };
  return colorMap[status] || 'default';
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
        return "日期无效";
    }
    return date.toLocaleString('zh-CN', options);
  } catch (e) {
    return "日期解析错误";
  }
};

const fetchOrderDetail = async () => {
  isLoading.value = true;
  if (!route.params.id) {
    message.error('订单ID无效');
    router.replace('/home'); 
    isLoading.value = false;
    return;
  }
  try {
    const response = await orderAPI.getOrderDetails(route.params.id);
    if (response.data && response.data.success && response.data.data) {
      const fetchedOrder = response.data.data;
      order.value = {
        total_amount: 0,
        coupon_discount: 0,
        actual_amount: 0,
        ...fetchedOrder
      };
    } else {
      message.error(response.data.message || '获取订单详情失败');
      order.value = null;
    }
  } catch (error) {
    message.error(error.message || '获取订单详情网络请求失败');
    order.value = null;
  } finally {
    isLoading.value = false;
  }
};

// 其他现有的处理函数保持不变...
const handleCancelOrder = async () => {
  if (!order.value || !order.value.id) return;
  try {
    if (!confirm('您确定要取消此订单吗？')) return;
    const response = await orderAPI.cancelOrder(order.value.id);
    if (response.data && response.data.success) {
        message.success('订单已取消');
        fetchOrderDetail(); 
    } else {
        message.error(response.data.message || '取消订单操作未成功');
    }
  } catch (error) {
    message.error(error.message || '取消订单失败');
  }
};

const handleReviewOrder = () => {
  if (!order.value || !order.value.id) return;
  const rating = prompt('请输入评价星级 (1-5):');
  if (rating === null) return; 
  const comment = prompt('请输入评价内容:');
  if (comment === null) return; 
  
  const parsedRating = parseInt(rating);
  if (rating && comment && !isNaN(parsedRating) && parsedRating >= 1 && parsedRating <= 5) {
    submitReview(parsedRating, comment);
  } else {
    message.warning('请输入有效的评价星级 (1-5的数字) 和评价内容。');
  }
};

const submitReview = async (rating, comment) => {
    try {
        const response = await orderAPI.reviewOrder(order.value.id, { rating, comment });
        if (response.data && response.data.success) {
            message.success('评价成功');
            fetchOrderDetail(); 
        } else {
            message.error(response.data.message || '评价提交失败');
        }
    } catch (error) {
        message.error(error.message || '评价请求失败');
    }
};

const handleDeleteOrder = async () => {
  if (!order.value || !order.value.id) return;
  try {
    if (!confirm('您确定要删除此订单吗？此操作无法撤销。')) return;
    const response = await orderAPI.deleteOrder(order.value.id);
    if (response.data && response.data.success) {
        message.success('订单已删除');
        router.push('/home'); 
    } else {
        message.error(response.data.message || '删除订单操作未成功');
    }
  } catch (error) {
    message.error(error.message || '删除订单失败');
  }
};

const handleCompleteOrder = async () => {
  if (!order.value || !order.value.id) return;
  try {
    if (!confirm('确认已收到物品吗？')) return;
    
    const response = await orderAPI.completeOrder(order.value.id);
    if (response.data && response.data.success) {
      message.success('订单已完成');
      fetchOrderDetail();
    } else {
      message.error(response.data.message || '完成订单操作未成功');
    }
  } catch (error) {
    message.error(error.message || '完成订单失败');
  }
};

const setPreviewVisible = (value) => {
  previewVisible.value = value;
};

onMounted(() => {
  fetchOrderDetail();
});
</script>
<style scoped>
.order-detail-container {
  display: flex;
  flex-direction: column;
  max-height: 900px;
  background-color: var(--color-bg-layout);
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollable-content::-webkit-scrollbar {
  display: none;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 卡片基础样式 */
.order-card,
.deliverer-card {
  margin-bottom: 16px;
  border-radius: 12px;
  box-shadow: var(--box-shadow-sm);
  border: 1px solid var(--color-border-secondary);
  transition: all 0.2s ease;
}

.order-card:hover {
  box-shadow: var(--box-shadow);
  border-color: var(--color-primary);
}

/* 订单元信息 */
.order-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.status-tag {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 4px;
  margin-right: 8px;
}

.order-no,
.order-time {
  font-size: 12px;
  color: var(--color-text-tertiary);
  display: flex;
  align-items: center;
}

.order-time::before {
  content: "•";
  margin: 0 6px;
  color: var(--color-text-quaternary);
}

/* 路线信息 */
.order-route {
  position: relative;
  padding: 0 8px;
  margin: 24px 0;
}

.route-point {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}

.point-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: white;
  margin-right: 12px;
  flex-shrink: 0;
}

.route-point.start .point-icon {
  background-color: var(--color-success);
}

.route-point.end .point-icon {
  background-color: var(--color-primary);
}

.point-detail {
  flex: 1;
  min-width: 0;
}

.main-address {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: 4px;
  line-height: 1.4;
}

.detail-address {
  font-size: 12px;
  color: var(--color-text-secondary);
  padding: 4px 8px;
  background-color: var(--color-fill-alter);
  border-radius: 4px;
  display: inline-block;
  line-height: 1.4;
}

.route-line {
  position: absolute;
  left: 11px;
  top: 12px;
  height: calc(100% - 24px);
  width: 2px;
  background-color: var(--color-border);
  z-index: 0;
}

/* 配送预估 */
.delivery-estimate {
  margin: 24px 0;
  padding: 16px;
  background-color: var(--color-fill-alter);
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
}

.estimate-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.estimate-item {
  display: flex;
  flex-direction: column;
}

.estimate-item .label {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
}

.estimate-item .value {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-primary);
}

/* 订单图片 */
.order-image-section {
  margin: 24px 0;
}

.order-image-preview {
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  border: 1px solid var(--color-border);
}

.order-image-preview:hover {
  transform: scale(1.02);
}

/* 信息区块 */
.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.section-title::before {
  content: "";
  display: inline-block;
  width: 4px;
  height: 14px;
  background-color: var(--color-primary);
  margin-right: 8px;
  border-radius: 2px;
}

.info-grid {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 13px;
}

.info-item .label {
  color: var(--color-text-secondary);
  margin-right: 12px;
  flex-shrink: 0;
}

.info-item .value {
  color: var(--color-text);
  text-align: right;
  word-break: break-word;
}

/* 金额信息 */
.order-amount {
  background-color: var(--color-fill-alter);
  border-radius: 8px;
  padding: 16px;
}

.amount-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 13px;
}

.amount-item.total {
  border-top: 1px solid var(--color-border);
  margin-top: 8px;
  padding-top: 12px;
  font-weight: 500;
}

.total-amount {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-error);
}

/* 配送员信息 */
.deliverer-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.deliverer-detail {
  flex: 1;
}

.deliverer-detail .name {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
}

.rating-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-text {
  font-size: 13px;
  color: var(--color-warning);
}

/* 操作按钮 */
.action-buttons {
  display: grid;
  gap: 12px;
  margin-top: 24px;
}

.action-buttons .ant-btn {
  height: 44px;
  border-radius: 8px;
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--color-text-secondary);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .estimate-info {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
}
</style>