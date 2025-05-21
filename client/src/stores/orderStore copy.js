import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import information from '@/assets/information.json'

export const useOrderStore = defineStore('order', () => {
  const activeTab = ref('home')
  const orders = ref([])
  const imageFailed = ref(false)
  const selectedOrders = ref([]) // 选中的订单数组
  const selectAll = ref(false) // 全选状态
  const requests = ref([]) // 委托请求数组

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

  // 添加新的委托请求
  function addRequest() {
    const newRequest = {
      id: requests.value.length + 1,
      origin: '',
      destination: '',
      description: '',
      image: null,
      orderInfo: '',
      amount: 0
    }
    requests.value.push(newRequest)
    console.log('当前请求列表：', requests.value) // 添加日志
    return newRequest
  }

  function publishNewOrder() {
    console.log('发布新委托')
  }

  function handleImageError() {
    imageFailed.value = true
  }

  function toggleSelectAll(isSelected) {
    selectAll.value = isSelected
    if (isSelected) {
      selectedOrders.value = [...orders.value]
    } else {
      selectedOrders.value = []
    }
  }

  function toggleOrderSelection(order) {
    const index = selectedOrders.value.findIndex(o => o.id === order.id)
    if (index === -1) {
      selectedOrders.value.push(order)
    } else {
      selectedOrders.value.splice(index, 1)
    }
    selectAll.value = selectedOrders.value.length === orders.value.length
  }

  const totalAmount = computed(() => {
    return selectedOrders.value.reduce((sum, order) => sum + (order.amount || 0), 0)
  })

  return {
    activeTab,
    orders,
    imageFailed,
    selectedOrders,
    selectAll,
    requests, // 导出 requests
    groupedOrders,
    totalAmount,
    loadOrders,
    handleTabChange,
    publishNewOrder,
    handleImageError,
    toggleSelectAll,
    toggleOrderSelection,
    addRequest, // 导出 addRequest 方法
  }
})
