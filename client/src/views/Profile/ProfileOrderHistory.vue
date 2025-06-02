<template>
  <div class="profile-order-history">
    <ProfileOrderHeader />
    <a-layout class="home-layout">
      <a-layout-content class="home-content">
        <order-history 
          @publish="publishNewOrder"
          @cancel="handleCancelOrder"
          @review="handleReviewOrder"
          @delete="handleDeleteOrder"
        />
      </a-layout-content>
    </a-layout>

    <!-- 取消订单确认对话框 -->
    <a-modal
      v-model:open="cancelModalVisible"
      title="确认取消订单"
      :confirm-loading="cancelLoading"
      @ok="confirmCancelOrder"
      @cancel="cancelModalVisible = false"
      ok-text="确认取消"
      cancel-text="取消"
    >
      <div class="modal-content">
        <a-typography-text type="warning">
          <exclamation-circle-outlined style="margin-right: 8px;" />
          您确定要取消这个订单吗？
        </a-typography-text>
        <div style="margin-top: 12px;">
          <a-typography-text type="secondary">
            订单取消后将无法恢复，请确认您的操作。
          </a-typography-text>
        </div>
      </div>
    </a-modal>

    <!-- 删除订单确认对话框 -->
    <a-modal
      v-model:open="deleteModalVisible"
      title="确认删除订单"
      :confirm-loading="deleteLoading"
      @ok="confirmDeleteOrder"
      @cancel="deleteModalVisible = false"
      ok-text="确认删除"
      cancel-text="取消"
      ok-type="danger"
    >
      <div class="modal-content">
        <a-typography-text type="danger">
          <delete-outlined style="margin-right: 8px;" />
          您确定要永久删除这个订单吗？
        </a-typography-text>
        <div style="margin-top: 12px;">
          <a-typography-text type="secondary">
            订单删除后将无法恢复，此操作不可撤销。
          </a-typography-text>
        </div>
      </div>
    </a-modal>

    <!-- 评价订单对话框 -->
    <a-modal
      v-model:open="reviewModalVisible"
      title="订单评价"
      :confirm-loading="reviewLoading"
      @ok="confirmReviewOrder"
      @cancel="reviewModalVisible = false"
      ok-text="提交评价"
      cancel-text="取消"
      width="400px"
    >
      <div class="review-form">
        <div class="form-item">
          <label>评分：</label>
          <a-rate v-model:value="reviewForm.rating" allow-half />
          <span style="margin-left: 8px;">{{ reviewForm.rating }} 星</span>
        </div>
        <div class="form-item">
          <label>评价内容：</label>
          <a-textarea
            v-model:value="reviewForm.comment"
            placeholder="请输入您的评价..."
            :rows="4"
            show-count
            :maxlength="200"
          />
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/orderStore';
import OrderHistory from '@/components/Home/HomeOrderhistory.vue';
import { message } from 'ant-design-vue';
import ProfileOrderHeader from '@/components/Header/ProfileOrderHeader.vue';
import { ExclamationCircleOutlined, DeleteOutlined } from '@ant-design/icons-vue';

const router = useRouter();
const orderStore = useOrderStore();

// 对话框状态
const cancelModalVisible = ref(false);
const deleteModalVisible = ref(false);
const reviewModalVisible = ref(false);

// 加载状态
const cancelLoading = ref(false);
const deleteLoading = ref(false);
const reviewLoading = ref(false);

// 当前操作的订单ID
const currentOrderId = ref(null);

// 评价表单
const reviewForm = reactive({
  rating: 5,
  comment: ''
});

onMounted(() => {
  orderStore.loadOrders();
});

const handleCancelOrder = async (orderId) => {
  currentOrderId.value = orderId;
  cancelModalVisible.value = true;
};

const confirmCancelOrder = async () => {
  cancelLoading.value = true;
  try {
    await orderStore.cancelOrder(currentOrderId.value);
    message.success('订单已取消');
    cancelModalVisible.value = false;
  } catch (error) {
    message.error(error.message || '取消订单失败');
  } finally {
    cancelLoading.value = false;
  }
};

const handleReviewOrder = async (orderId) => {
  currentOrderId.value = orderId;
  // 重置表单
  reviewForm.rating = 5;
  reviewForm.comment = '';
  reviewModalVisible.value = true;
};

const confirmReviewOrder = async () => {
  if (!reviewForm.comment.trim()) {
    message.warning('请输入评价内容');
    return;
  }
  
  reviewLoading.value = true;
  try {
    await orderStore.reviewOrder(currentOrderId.value, {
      rating: reviewForm.rating,
      comment: reviewForm.comment.trim()
    });
    message.success('评价成功');
    reviewModalVisible.value = false;
  } catch (error) {
    message.error(error.message || '评价失败');
  } finally {
    reviewLoading.value = false;
  }
};

const handleDeleteOrder = async (orderId) => {
  currentOrderId.value = orderId;
  deleteModalVisible.value = true;
};

const confirmDeleteOrder = async () => {
  deleteLoading.value = true;
  try {
    await orderStore.deleteOrder(currentOrderId.value);
    message.success('订单已删除');
    deleteModalVisible.value = false;
  } catch (error) {
    message.error(error.message || '删除订单失败');
  } finally {
    deleteLoading.value = false;
  }
};

const publishNewOrder = () => {
  router.push('/publish');
};
</script>

<style scoped>
.profile-order-history {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100vh;
  max-height: 840px;
}

.home-layout {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.home-content {
  height: 100%;
  overflow-y: auto;
}

.modal-content {
  padding: 16px 0;
}

.review-form {
  padding: 16px 0;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-item .ant-rate {
  margin-bottom: 4px;
}
</style>