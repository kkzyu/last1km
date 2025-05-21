<template>
  <HomeHead />
  <div class="home-page">
    <HomeCarousel />
    <OrderHistory 
      :grouped-orders="groupedOrders"
      @publish="publishNewOrder"
      @cancel="cancelOrder"
      @restore="restoreOrder"  
      @review="reviewOrder"
    />
  </div>
  <BottomNav />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'  // 添加路由导入

const router = useRouter()  // 获取路由实例

import information from '@/assets/data/information.json'
import HomeCarousel from '@/components/Home/HomeCarousel.vue'
import OrderHistory from '@/components/Home/HomeOrderhistory.vue'
import HomeHead from '@/components/Header/HomeHead.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'

const activeTab = ref('home')
const orders = ref([])
const imageFailed = ref(false)

// 从localStorage加载订单数据
const loadOrders = () => {
  const savedOrders = localStorage.getItem('orders')
  orders.value = savedOrders ? JSON.parse(savedOrders) : information.orders
}

// 保存订单到localStorage
const saveOrders = () => {
  localStorage.setItem('orders', JSON.stringify(orders.value))
}

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

onMounted(() => {
  loadOrders()
})

const cancelOrder = (orderId) => {
  const order = orders.value.find(o => o.id === orderId)
  if (order && order.status === '进行中') {
    order.status = '已取消'
    order.description = "已取消" 
    order.eta = null
    saveOrders()
  }
}

const restoreOrder = (orderId) => {
  const order = orders.value.find(o => o.id === orderId)
  if (order && order.status === '已取消') {
    order.status = '进行中'
    order.description = ""  // 恢复描述为空
    order.eta = 20  // 恢复预计时间
    saveOrders()
  }
}

const reviewOrder = (orderId) => {
  console.log('评价订单:', orderId)
}

const publishNewOrder = () => {
  router.push('/publish') // 修改为正确的小写router
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
  height: 100%;
  background-color: #f4f4f4;
  overflow: hidden; 
}

.home-page > :first-child {
  flex-shrink: 0; 
}
</style>