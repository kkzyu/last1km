// views/Home/HomeView.vue
<template>
  <a-layout class="home-layout">
    <app-header />
    <a-layout-content class="home-content">
      <home-carousel />
      <order-history 
        @publish="publishNewOrder"
        @cancel="cancelOrder"
        @restore="restoreOrder"  
        @review="reviewOrder"
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
import OrderHistory from '@/components/Home/HomeOrderhistory.vue'; // 假设已重构
import AppHeader from '@/components/Header/HomeHead.vue';
import AppFooter from '@/components/Bottom/BottomNav.vue';

const router = useRouter();
const orderStore = useOrderStore();

onMounted(() => {
  orderStore.loadOrders();
});

const cancelOrder = (orderId) => {
  orderStore.cancelOrder(orderId);
};

const restoreOrder = (orderId) => {
  orderStore.restoreOrder(orderId);
};

const reviewOrder = (orderId) => {
  orderStore.reviewOrder(orderId);
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