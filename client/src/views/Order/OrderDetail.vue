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
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { orderAPI } from '@/api/api'; // 确保 api.js 中导出了 orderAPI
import { message, Image as AImage, Rate as ARate, Avatar as AAvatar, Spin as ASpin } from 'ant-design-vue'; // 按需导入 AImage 等
import { UserOutlined } from '@ant-design/icons-vue'; // 用于配送员默认头像
import OrderDetailHeader from '@/components/Header/OrderDetailHeader.vue';

const route = useRoute();
const router = useRouter();
const order = ref(null); // 确保已声明
const isLoading = ref(true);
const previewVisible = ref(false);

const API_BASE_URL = 'http://localhost:5000'; // 与其他地方保持一致

// getImageUrl现在可以接受一个可选参数isAvatar, 如果是头像且路径不是完整的，则不加/static/uploads
const getImageUrl = (imagePath, isFullPathOrAvatar = false) => {
  if (!imagePath) return '';
  if (isFullPathOrAvatar && (imagePath.startsWith('http') || imagePath.startsWith('/'))) {
    // 如果是完整的 URL (http/https) 或者已经是 /static/... 这样的相对路径 (虽然我们约定存文件名)
    // 或者是一个头像路径（可能来自不同地方）
    return imagePath; 
  }
  // 默认处理订单图片，拼接路径
  return `${API_BASE_URL}/static/uploads/${imagePath}`;
};


const getDisplayStatus = (status) => {
  const statusMap = {
    pending: '进行中',
    accepted: '已接单', // 新增状态示例
    delivering: '配送中', // 新增状态示例
    completed: '已完成',
    cancelled: '已取消',
    reviewed: '已评价' // 如果评价后会改变状态
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
  // 检查日期字符串是否已经是UTC格式（以Z结尾）
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
  try {
    const date = new Date(dateString);
    // 检查日期是否有效
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
    router.replace('/home'); // 或其他合适的路径
    isLoading.value = false;
    return;
  }
  try {
    const response = await orderAPI.getOrderDetails(route.params.id);
    // 假设后端 success_response 总是将数据包装在 response.data.data 中
    if (response.data && response.data.success && response.data.data) {
      const fetchedOrder = response.data.data;
      // 为金额字段提供默认值，以防后端未返回这些字段
      order.value = {
        total_amount: 0,
        coupon_discount: 0,
        actual_amount: 0,
        ...fetchedOrder // 后端数据会覆盖默认值
      };
    } else {
      message.error(response.data.message || '获取订单详情失败');
      order.value = null; // 清空订单数据
      // router.go(-1); // 可以选择是否返回上一页
    }
  } catch (error) {
    message.error(error.message || '获取订单详情网络请求失败');
    order.value = null;
    // router.go(-1);
  } finally {
    isLoading.value = false;
  }
};

const handleCancelOrder = async () => {
  console.log('Current order:', order.value);
  if (!order.value || !order.value.id) return;
  try {
    // 添加二次确认
    if (!confirm('您确定要取消此订单吗？')) return;
    
    const response = await orderAPI.cancelOrder(order.value.id);
    if (response.data && response.data.success) {
        message.success('订单已取消');
        fetchOrderDetail(); // 重新加载订单详情以更新状态
    } else {
        message.error(response.data.message || '取消订单操作未成功');
    }
  } catch (error) {
    message.error(error.message || '取消订单失败');
  }
};

const handleReviewOrder = () => {
  if (!order.value || !order.value.id) return;
  // 这里可以直接使用您已有的评价逻辑，例如弹窗
  // 为了演示，我们假设跳转到评价页面，但您也可以用Modal
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
            fetchOrderDetail(); // 重新加载以更新状态（例如，显示已评价或隐藏评价按钮）
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
    // 添加二次确认
    if (!confirm('您确定要删除此订单吗？此操作无法撤销。')) return;

    const response = await orderAPI.deleteOrder(order.value.id);
    if (response.data && response.data.success) {
        message.success('订单已删除');
        router.push('/home'); // 删除成功后返回首页或订单列表页
    } else {
        message.error(response.data.message || '删除订单操作未成功');
    }
  } catch (error) {
    message.error(error.message || '删除订单失败');
  }
};

// 图片预览控制
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
  height: 100vh;
  background-color: #f5f5f7; /* 保持浅灰色背景 */
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 50px;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.scrollable-content::-webkit-scrollbar {
  display: none;  /* Chrome, Safari and Opera */
}

.order-content {
  padding: 16px;
  min-height: calc(100vh - 150px); /* 减去头部和底部空间 */
}

.order-header {
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px; /* 或者根据需要设置更高 */
}

.order-content {
  padding: 16px;
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
  align-items: center;
  margin-bottom: 10px; /* 起点和终点之间的间距 */
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
.route-point.start .point-icon { background-color: #52c41a; } /* Ant Design success color */
.route-point.end .point-icon { background-color: #1890ff; } /* Ant Design primary color for end */

.route-point .point-detail {
  font-size: 15px;
  color: #333;
  line-height: 1.5;
}

.route-line {
  position: absolute;
  left: 13px; /* (28px / 2) - 1px for border */
  top: 28px; /* Start below the 'start' icon */
  bottom: 28px; /* End above the 'end' icon */
  width: 2px;
  background-color: #e8e8e8;
  z-index: 0;
}
/* 确保路线文本不与线重叠太多 */
.route-point.start + .route-line + .route-point.end {
    margin-top: 10px; /* 增加终点与起点的垂直间距 */
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
  max-width: 100%; /* 确保图片响应式 */
  height: auto;
  display: block; /* 移除图片下方的额外空间 */
  /* object-fit: cover; /* 如果想固定尺寸并裁剪 */
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
}
.info-item .value {
  color: #333;
  text-align: right;
  word-break: break-all; /* 长文本换行 */
}

.amount-item span:first-child { color: #555; }
.amount-item .amount, .amount-item .discount { color: #333; }
.amount-item.total {
  font-weight: 500;
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px solid #e8e8e8; /* 在总计前加一条实线 */
  border-bottom: none; /* 移除总计的虚线 */
}
.amount-item .total-amount {
  font-size: 18px;
  color: #fa541c; /* Ant Design warning color for emphasis */
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
  font-size: 16px; /* 调整星星大小 */
  margin-right: 8px;
}
.deliverer-detail .rating-text {
  color: #faad14; /* Ant Design warning color for rating text */
}

.action-buttons {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px; /* 按钮之间的间距 */
}
.action-buttons .ant-btn {
  height: 40px; /* 按钮高度 */
  font-size: 15px; /* 按钮字体大小 */
}
.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #888;
}
</style>
