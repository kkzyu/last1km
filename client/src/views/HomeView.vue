<template>
  <div class="home-page">
    <HomeCarousel />
    <OrderHistory 
      :grouped-orders="groupedOrders"
      @publish="publishNewOrder"
      @cancel="cancelOrder"
      @review="reviewOrder"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import information from '@/assets/information.json'
import HomeCarousel from '@/components/HomeCarousel.vue'
import OrderHistory from '@/components/OrderHistory.vue'

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
.home-page {
  font-family: sans-serif;
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f4f4;
}
</style>