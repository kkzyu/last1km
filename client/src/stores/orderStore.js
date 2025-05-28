import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import information from '@/assets/data/information.json'
import axios from 'axios';

export const useOrderStore = defineStore('order', () => {
  const activeTab = ref('home')
  const orders = ref([])
  const imageFailed = ref(false)
  const selectedOrders = ref([]) // 选中的订单数组
  const selectAll = ref(false) // 全选状态
  const requests = ref([]) // 委托请求数组
  const currentOrderDetail = ref(null);
  const loading = ref(false);

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

// 添加恢复订单方法
  async function restoreOrder(orderId) {
    try {
      const response = await axios.put(`/api/orders/${orderId}/restore`);
      // 更新本地订单状态
      const index = orders.value.findIndex(order => order.id === orderId);
      if (index !== -1) {
        orders.value[index].order_status = 'pending';
      }
      return response.data;
    } catch (error) {
      console.error('恢复订单失败:', error);
      throw error;
    }
  }
  
  // 添加订单详情获取方法
  async function fetchOrderDetail(orderId) {
    try {
      const response = await axios.get(`/api/orders/${orderId}`);
      currentOrderDetail.value = response.data.data;
      return response.data.data;
    } catch (error) {
      console.error('获取订单详情失败:', error);
      throw error;
    }
  }
  
  // 添加评价订单方法
  async function reviewOrder(orderId, reviewData) {
    try {
      const response = await axios.post(`/api/orders/${orderId}/review`, reviewData);
      return response.data;
    } catch (error) {
      console.error('评价订单失败:', error);
      throw error;
    }
  }
  
  // 添加取消订单方法
  async function cancelOrder(orderId) {
    try {
      const response = await axios.put(`/api/orders/${orderId}/cancel`);
      // 更新本地订单状态
      const index = orders.value.findIndex(order => order.id === orderId);
      if (index !== -1) {
        orders.value[index].order_status = 'cancelled';
      }
      return response.data;
    } catch (error) {
      console.error('取消订单失败:', error);
      throw error;
    }
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
    fetchOrderDetail,
    reviewOrder,
    restoreOrder,
    cancelOrder,
  }
})
