import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import information from '@/assets/information.json'

export const useOrderStore = defineStore('order', () => {
  const activeTab = ref('home')
  const orders = ref([])
  const imageFailed = ref(false)

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

  function loadOrders() {
    orders.value = information.orders
  }

  function handleTabChange(tab) {
    activeTab.value = tab
    console.log('切换到标签:', tab)
  }

  function publishNewOrder() {
    console.log('发布新委托')
  }

  function handleImageError() {
    imageFailed.value = true
  }

  return {
    activeTab,
    orders,
    imageFailed,
    groupedOrders,
    loadOrders,
    handleTabChange,
    publishNewOrder,
    handleImageError
  }
})
