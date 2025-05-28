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

          <div class="order-route">
            <div class="route-point start">
              <div class="point-icon">起</div>
              <div class="point-detail">{{ order.start_address }}</div>
            </div>
            <div class="route-line"></div>
            <div class="route-point end">
              <div class="point-icon">终</div>
              <div class="point-detail">{{ order.end_address }}</div>
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
            <div class="info-item" v-if="order.locker_number">
              <span class="label">储物柜号:</span>
              <span class="value">{{ order.locker_number }}</span>
            </div>
          </div>

          <a-divider />

          <div class="order-amount">
            <h3 class="section-title">金额明细</h3>
            <div class="amount-item">
              <span>订单金额:</span>
              <span class="amount">¥{{ order.total_amount != null ? order.total_amount.toFixed(2) : '0.00' }}</span>
            </div>
            <div class="amount-item" v-if="order.coupon_discount != null && order.coupon_discount > 0">
              <span>优惠券减免:</span>
              <span class="discount">-¥{{ order.coupon_discount.toFixed(2) }}</span>
            </div>
            <div class="amount-item total">
              <span>实付金额:</span>
              <span class="total-amount">¥{{ order.actual_amount != null ? order.actual_amount.toFixed(2) : '0.00' }}</span>
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

<script setup> // <--- 所有逻辑都应在此处或通过导入模块的方式
import { ref, onMounted } from 'vue'; // computed 未使用，已移除
import { useRoute, useRouter } from 'vue-router';
import { orderAPI } from '@/api/api';
import { message, Image as AImage, Rate as ARate, Avatar as AAvatar, Spin as ASpin } from 'ant-design-vue';
import { UserOutlined } from '@ant-design/icons-vue';
import OrderDetailHeader from '@/components/Header/OrderDetailHeader.vue'; // 确保这个组件已创建并正确导入

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
      fetchOrderDetail(); // 重新加载订单详情
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
/* 您的CSS样式保持不变 */
.order-detail-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 改为视口高度，确保内容区可滚动 */
  background-color: #f5f5f7; 
}

.scrollable-content { /* 新增包裹层用于滚动 */
  flex: 1;
  overflow-y: auto;
  /* padding-bottom: 50px; 为可能的底部操作栏预留空间（如果OrderDetailHeader不是fixed） */
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.scrollable-content::-webkit-scrollbar { /* Chrome, Safari and Opera */
  display: none;
}


.order-header { /* 如果头部是fixed或sticky，需要调整scrollable-content的padding-top */
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  /* position: sticky; top: 0; z-index: 10; 如果希望头部吸顶 */
}
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px; 
  padding-top: 50px; /* 确保在头部下方可见 */
}

.order-content {
  padding: 16px;
  /* min-height: calc(100vh - 150px); */ /* 如果头部和底部有固定高度，可以这样计算 */
}

.order-card, .deliverer-card, .section-card {
  margin-bottom: 16px;
  border-radius: 8px;
}

.order-meta {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.status-tag {
  font-size: 14px;
  padding: 4px 10px;
  margin-bottom: 10px;
}

.order-no, .order-time {
  font-size: 13px;
  color: #888;
  margin-bottom: 4px;
  line-height: 1.6;
}

.order-route {
  margin: 20px 0;
  position: relative;
}

.route-point {
  display: flex;
  align-items: flex-start; /* 改为flex-start使图标和多行文本顶部对齐 */
  margin-bottom: 10px; 
}

.route-point .point-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: white;
  margin-right: 12px;
  flex-shrink: 0;
}
.route-point.start .point-icon { background-color: #52c41a; } 
.route-point.end .point-icon { background-color: #1890ff; } 

.route-point .point-detail {
  font-size: 15px;
  color: #333;
  line-height: 1.5;
  word-break: break-word; /* 允许长地址换行 */
}

.route-line {
  position: absolute;
  left: 13px; 
  top: 14px; /* 从第一个图标中心开始 */
  height: calc(100% - 28px); /* 连接两个图标中心 */
  width: 2px;
  background-color: #e8e8e8;
  z-index: 0;
}
.order-image-section {
    margin-top: 20px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    margin-bottom: 12px;
}
.order-image-preview {
  border-radius: 6px;
  max-width: 100%; 
  height: auto;
  display: block; 
}

.order-info, .order-amount {
  margin: 20px 0;
}
.info-item, .amount-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
  color: #555;
  border-bottom: 1px dashed #f0f0f0;
}
.info-item:last-child, .amount-item:last-child {
  border-bottom: none;
}
.info-item .label {
  color: #888;
  margin-right: 8px;
  white-space: nowrap;
  flex-shrink: 0; /* 防止标签被压缩 */
}
.info-item .value {
  color: #333;
  text-align: right;
  word-break: break-all; 
}

.amount-item span:first-child { color: #555; }
.amount-item .amount, .amount-item .discount { color: #333; }
.amount-item.total {
  font-weight: 500;
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px solid #e8e8e8; 
  border-bottom: none; 
}
.amount-item .total-amount {
  font-size: 18px;
  color: #fa541c; 
}

.deliverer-card .deliverer-info {
  display: flex;
  align-items: center;
}
.deliverer-info .ant-avatar {
  margin-right: 16px;
}
.deliverer-detail .name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}
.deliverer-detail .rating {
  display: flex;
  align-items: center;
  font-size: 13px;
}
.deliverer-detail .rating .ant-rate {
  font-size: 16px; 
  margin-right: 8px;
}
.deliverer-detail .rating-text {
  color: #faad14; 
}

.action-buttons {
  margin-top: 24px;
  padding: 0 16px 16px 16px; /* 在内容区底部增加内边距 */
  /* 如果希望按钮固定在底部，需要不同的布局方式 */
  display: flex;
  flex-direction: column;
  gap: 12px; 
}
.action-buttons .ant-btn {
  height: 44px; /* 按钮高度略微增加 */
  font-size: 16px; /* 按钮字体大小略微增加 */
  border-radius: 8px; /* 按钮圆角 */
}
.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #888;
  min-height: 200px; /* 确保空状态时也有一定高度 */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>