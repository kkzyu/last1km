<template>
  <a-layout class="home-layout">
    <app-header />
    <a-layout-content class="home-content">
      <home-carousel />
      <order-history 
        @publish="publishNewOrder"
        @cancel="handleCancelOrder"
        @review="handleReviewOrder"
        @delete="handleDeleteOrder"
      />
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/orderStore';
import HomeCarousel from '@/components/Home/HomeCarousel.vue';
import OrderHistory from '@/components/Home/HomeOrderhistory.vue';
import AppHeader from '@/components/Header/HomeHead.vue';
import AppFooter from '@/components/Bottom/BottomNav.vue';
import { message } from 'ant-design-vue';

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
.home-layout {
  min-height: 900px;
  background-color: #f5f5f7;
  display: flex;
  flex-direction: column;
}

.home-content {
  /* padding-bottom: 60px; 为底部导航留出空间 */
  background-color: #f4f4f4;
  flex:1;
  flex-direction: column;
  display:flex;
  overflow:hidden;
  
}
</style>