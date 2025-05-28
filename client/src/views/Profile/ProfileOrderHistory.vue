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
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/orderStore';
import OrderHistory from '@/components/Home/HomeOrderhistory.vue';
import { message } from 'ant-design-vue';
import ProfileOrderHeader from '@/components/Header/ProfileOrderHeader.vue';

const router = useRouter();
const orderStore = useOrderStore();

onMounted(() => {
  orderStore.loadOrders();
});

const handleCancelOrder = async (orderId) => {
  try {
    await orderStore.cancelOrder(orderId);
    message.success('订单已取消');
  } catch (error) {
    message.error(error.message || '取消订单失败');
  }
};

const handleReviewOrder = async (orderId) => {
  try {
    const ratingInput = prompt('请输入评价星级 (1-5):');
    if (ratingInput === null) return; 

    const comment = prompt('请输入评价内容:');
    if (comment === null) return; 
    
    const rating = parseInt(ratingInput);
    if (ratingInput && comment && !isNaN(rating) && rating >= 1 && rating <= 5) {
      await orderStore.reviewOrder(orderId, { rating: rating, comment });
      message.success('评价成功');
    } else {
      message.warning('请输入有效的评价星级 (1-5的数字) 和评价内容。');
    }
  } catch (error) {
    message.error(error.message || '评价失败');
  }
};

const handleDeleteOrder = async (orderId) => {
  try {
    //可以添加二次确认
    if (!confirm('确定要删除此订单吗？')) return;
    await orderStore.deleteOrder(orderId);
    message.success('订单已删除');
  } catch (error) {
    message.error(error.message || '删除订单失败');
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
  min-height: 100vh; /* 至少填满屏幕 */
  max-height: 840px; /* 移除最大高度限制 */
}

.home-layout {
  flex: 1;
  min-height: 0;
  overflow: hidden; /* 防止内容溢出 */
}

.home-content {
  height: 100%;
  overflow-y: auto;
}
</style>