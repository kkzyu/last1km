<template>
  <a-layout class="order-detail-layout">
    <app-header title="订单详情" :show-back="true" />
    
    <a-layout-content class="order-detail-content">
      <a-spin :spinning="isLoading">
        <div v-if="error" class="error-message">
          <a-alert :message="error" type="error" />
        </div>
        
        <template v-else-if="orderDetails">
          <!-- 订单头部信息 -->
          <a-card class="order-card">
            <div class="order-header">
              <div class="order-status">
                <a-tag :color="getStatusColor(orderDetails.order_status)">
                  {{ getStatusText(orderDetails.order_status) }}
                </a-tag>
                <span class="order-id">订单号: {{ orderDetails.id }}</span>
              </div>
              <span class="order-date">{{ formatDate(orderDetails.created_at) }}</span>
            </div>
            
            <!-- 订单截图 -->
            <div class="order-image" v-if="orderDetails.image_url">
              <img :src="orderDetails.image_url" alt="订单截图" @click="previewImage">
            </div>
            
            <!-- 地址信息 -->
            <div class="address-info">
              <div class="address-item">
                <div class="address-icon start">起</div>
                <div class="address-content">
                  <div class="address-label">取件地点</div>
                  <div class="address-value">{{ orderDetails.start_address }}</div>
                </div>
              </div>
              
              <div class="address-item">
                <div class="address-icon end">终</div>
                <div class="address-content">
                  <div class="address-label">送达地点</div>
                  <div class="address-value">{{ orderDetails.end_address }}</div>
                </div>
              </div>
            </div>
            
            <!-- 物品信息 -->
            <div class="item-info">
              <h4>物品描述</h4>
              <p>{{ orderDetails.item_description || '未提供描述' }}</p>
              
              <h4>取件信息</h4>
              <p v-if="orderDetails.pickup_code || orderDetails.locker_number">
                {{ orderDetails.locker_number ? `柜号: ${orderDetails.locker_number}` : '' }}
                {{ orderDetails.pickup_code ? `取件码: ${orderDetails.pickup_code}` : '' }}
              </p>
              <p v-else>未提供取件信息</p>
            </div>
          </a-card>
          
          <!-- 配送员信息 -->
          <a-card class="rider-card" v-if="orderDetails.deliverer">
            <div class="rider-info" @click="navigateToRiderProfile(orderDetails.deliverer.id)">
              <a-avatar :src="orderDetails.deliverer.avatar" :size="50">
                {{ orderDetails.deliverer.name ? orderDetails.deliverer.name[0] : 'R' }}
              </a-avatar>
              <div class="rider-details">
                <div class="rider-name">{{ orderDetails.deliverer.name }}</div>
                <div class="rider-rating">
                  <a-rate :value="orderDetails.deliverer.rating" disabled allow-half :count="5" />
                  <span>{{ orderDetails.deliverer.rating.toFixed(1) }}</span>
                </div>
              </div>
              <a-button type="primary" @click.stop="contactRider">联系配送员</a-button>
            </div>
          </a-card>
          
          <!-- 费用明细 -->
          <a-card class="price-card">
            <h4>费用明细</h4>
            <div class="price-item">
              <span>配送费</span>
              <span>¥{{ orderDetails.total_amount.toFixed(2) }}</span>
            </div>
            <div class="price-item" v-if="orderDetails.coupon_discount > 0">
              <span>优惠券</span>
              <span>-¥{{ orderDetails.coupon_discount.toFixed(2) }}</span>
            </div>
            <div class="price-item total">
              <span>实付金额</span>
              <span>¥{{ orderDetails.actual_amount.toFixed(2) }}</span>
            </div>
          </a-card>
          
          <!-- 评价区域 -->
          <a-card class="review-card" v-if="orderDetails.order_status === 'completed'">
            <h4>订单评价</h4>
            <div v-if="orderDetails.review" class="existing-review">
              <div class="review-rating">
                <span>您的评分:</span>
                <a-rate :value="orderDetails.review.rating" disabled allow-half />
              </div>
              <div class="review-comment" v-if="orderDetails.review.comment">
                <p>{{ orderDetails.review.comment }}</p>
              </div>
            </div>
            <div v-else class="add-review">
              <p>您尚未评价此订单</p>
              <a-button type="primary" @click="showReviewModal">立即评价</a-button>
            </div>
          </a-card>
          
          <!-- 操作按钮 -->
          <div class="action-buttons">
            <a-button 
              v-if="orderDetails.order_status === 'pending'" 
              type="danger" 
              @click="cancelOrder"
            >
              取消订单
            </a-button>
            <a-button 
              v-if="orderDetails.order_status === 'cancelled'" 
              type="primary" 
              @click="restoreOrder"
            >
              恢复订单
            </a-button>
          </div>
        </template>
      </a-spin>
    </a-layout-content>
    
    <app-footer />
    
    <!-- 评价弹窗 -->
    <a-modal
      v-model:visible="reviewModalVisible"
      title="评价订单"
      @ok="submitReview"
      :confirmLoading="submittingReview"
    >
      <div class="review-form">
        <div class="rating-select">
          <span>您的评分:</span>
          <a-rate v-model:value="reviewRating" allow-half />
        </div>
        <a-textarea
          v-model:value="reviewComment"
          placeholder="请输入您的评价内容(可选)"
          :rows="4"
        />
      </div>
    </a-modal>
    
    <!-- 图片预览 -->
    <a-image
      :width="200"
      :style="{ display: 'none' }"
      :src="orderDetails?.image_url"
      :preview="{
        visible: previewVisible,
        onVisibleChange: (vis) => previewVisible = vis,
      }"
    />
  </a-layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { useOrderStore } from '@/stores/orderStore';
import AppHeader from '@/components/Header/BackHeader.vue';
import AppFooter from '@/components/Bottom/BottomNav.vue';

const route = useRoute();
const router = useRouter();
const orderStore = useOrderStore();
const orderId = computed(() => route.params.id);

const orderDetails = ref(null);
const isLoading = ref(true);
const error = ref(null);
const previewVisible = ref(false);
const reviewModalVisible = ref(false);
const reviewRating = ref(5);
const reviewComment = ref('');
const submittingReview = ref(false);

// 加载订单详情
onMounted(async () => {
  try {
    isLoading.value = true;
    await orderStore.fetchOrderDetail(orderId.value);
    orderDetails.value = orderStore.currentOrderDetail;
    if (!orderDetails.value) {
      error.value = '未找到订单详情';
    }
  } catch (err) {
    error.value = '加载订单详情失败: ' + err.message;
  } finally {
    isLoading.value = false;
  }
});

// 订单状态显示
const getStatusColor = (status) => {
  const statusMap = {
    pending: 'orange',
    accepted: 'blue',
    delivering: 'processing',
    completed: 'success',
    cancelled: 'error'
  };
  return statusMap[status] || 'default';
};

const getStatusText = (status) => {
  const statusMap = {
    pending: '待接单',
    accepted: '已接单',
    delivering: '配送中',
    completed: '已完成',
    cancelled: '已取消'
  };
  return statusMap[status] || '未知状态';
};

// 日期格式化
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 操作函数
const previewImage = () => {
  previewVisible.value = true;
};

const showReviewModal = () => {
  reviewModalVisible.value = true;
};

const submitReview = async () => {
  if (reviewRating.value === 0) {
    message.error('请至少给出评分');
    return;
  }
  
  try {
    submittingReview.value = true;
    await orderStore.reviewOrder(orderId.value, {
      rating: reviewRating.value,
      comment: reviewComment.value
    });
    
    message.success('评价提交成功');
    reviewModalVisible.value = false;
    
    // 刷新订单详情
    await orderStore.fetchOrderDetail(orderId.value);
    orderDetails.value = orderStore.currentOrderDetail;
  } catch (err) {
    message.error('评价提交失败: ' + err.message);
  } finally {
    submittingReview.value = false;
  }
};

const cancelOrder = async () => {
  try {
    await orderStore.cancelOrder(orderId.value);
    message.success('订单已取消');
    await orderStore.fetchOrderDetail(orderId.value);
    orderDetails.value = orderStore.currentOrderDetail;
  } catch (err) {
    message.error('取消订单失败: ' + err.message);
  }
};

const restoreOrder = async () => {
  try {
    await orderStore.restoreOrder(orderId.value);
    message.success('订单已恢复');
    await orderStore.fetchOrderDetail(orderId.value);
    orderDetails.value = orderStore.currentOrderDetail;
  } catch (err) {
    message.error('恢复订单失败: ' + err.message);
  }
};

const navigateToRiderProfile = (riderId) => {
  router.push(`/rider/${riderId}/profile`);
};

const contactRider = () => {
  if (orderDetails.value?.deliverer?.id) {
    router.push(`/messages/chat/chat_${orderDetails.value.deliverer.id}`);
  }
};
</script>

<style scoped>
.order-detail-layout {
  min-height: 100vh;
  background-color: #f5f5f7;
}

.order-detail-content {
  padding: 16px;
  padding-bottom: 70px;
}

.error-message {
  margin: 20px 0;
}

.order-card, .rider-card, .price-card, .review-card {
  margin-bottom: 16px;
  border-radius: 10px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.order-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.order-date {
  color: #999;
  font-size: 14px;
}

.order-image {
  margin: 16px 0;
  text-align: center;
}

.order-image img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  cursor: pointer;
}

.address-info {
  margin: 16px 0;
}

.address-item {
  display: flex;
  margin-bottom: 16px;
}

.address-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  margin-right: 12px;
  flex-shrink: 0;
}

.address-icon.start {
  background-color: #1890ff;
}

.address-icon.end {
  background-color: #52c41a;
}

.address-content {
  flex: 1;
}

.address-label {
  color: #999;
  font-size: 14px;
}

.address-value {
  font-weight: 500;
}

.item-info {
  margin: 16px 0;
}

.item-info h4 {
  margin-bottom: 8px;
  color: #333;
}

.rider-info {
  display: flex;
  align-items: center;
  padding: 8px 0;
  cursor: pointer;
}

.rider-details {
  flex: 1;
  margin-left: 16px;
}

.rider-name {
  font-weight: 500;
  font-size: 16px;
}

.rider-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-card h4 {
  margin-bottom: 16px;
}

.price-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.price-item.total {
  font-weight: bold;
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
  margin-top: 12px;
}

.review-card h4 {
  margin-bottom: 16px;
}

.existing-review .review-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-review {
  text-align: center;
}

.action-buttons {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.review-form .rating-select {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.review-form .rating-select span {
  margin-right: 16px;
}
</style>