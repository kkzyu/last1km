<template>
  <HomeHead />
  <div class="home-page">
    <HomeCarousel />
    <OrderHistory :grouped-orders="groupedOrders" @publish="publishNewOrder" @cancel="cancelOrder"
      @review="reviewOrder" />
  </div>
  <BottomNav />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import information from '@/assets/data/information.json'
import HomeCarousel from '@/components/Home/HomeCarousel.vue'
import OrderHistory from '@/components/Home/HomeOrderhistory.vue'
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

// 状态管理
const activeTab = ref('home')
const orders = ref([])
const imageFailed = ref(false)

// 计算属性
const groupedOrders = computed(() => {
  const groups = {}
  orders.value.forEach(order => {
    if (!groups[order.date]) {
      groups[order.date] = []
    }
    groups[order.date].push(order)
  })
  return groups
})

// 生命周期钩子
onMounted(() => {
  orders.value = information.orders
})

// 事件处理函数
const handleTabChange = (tab) => {
  console.log('切换到标签:', tab)
}

const cancelOrder = (orderId) => {
  console.log('取消订单:', orderId)
}

const reviewOrder = (orderId) => {
  console.log('评价订单:', orderId)
}

const publishNewOrder = () => {
  console.log('发布新委托')
}

const handleImageError = () => {
  imageFailed.value = true
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 750px;
  max-width: 500px;
  margin: 0 auto;
}

.content-container {
  flex: 1;
  overflow: hidden;
  position: relative;

}

.home-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  /* 启用整体滚动 */
}

.scrolling-banner {
  width: 100%;
  margin-bottom: 20px;
  /* 添加与内容的间距 */
}

/* 订单历史容器调整 */
.home-page> :last-child {
  flex: 1;
  min-height: 0;
  /* 允许内容收缩 */
}
</style>