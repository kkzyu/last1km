import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { orderAPI } from '@/api/api'

export const useOrderStore = defineStore('order', () => {
  const activeTab = ref('home')
  const orders = ref([])
  const requests = ref([])
  const isLoading = ref(false);
  const error = ref(null);

  const groupedOrders = computed(() => {
    const groups = {}
    const sortedOrders = [...orders.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    sortedOrders.forEach(order => {
      const date = new Date(order.created_at).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
      if (!groups[date]) {
        groups[date] = []
      }
      groups[date].push(order)
    })
    return groups
  })

  async function loadOrders() {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await orderAPI.getOrders(); // 后端已过滤
      if (response.data && Array.isArray(response.data.data)) {
        orders.value = response.data.data;
      } else if (Array.isArray(response.data)) {
         orders.value = response.data;
      } else {
        orders.value = [];
      }
    } catch (err) {
      console.error('加载订单失败 (Store):', err);
      error.value = err.message || '加载订单数据时出错';
      orders.value = [];
    } finally {
      isLoading.value = false;
    }
  }

  function handleTabChange(tab) {
    activeTab.value = tab
  }
  
  function addRequest() {
    const newRequest = {
      id: requests.value.length + 1,
      origin: '',
      destination: '',
      description: '',
      orderInfo: '',
      image: null,
      amount: 0,
      selected: true
    }
    requests.value.push(newRequest)
    return newRequest
  }


  async function publishNewOrder(requestData) {
    try {
      if (!requestData.selected) {
        return { success: true, message: '跳过未选中的委托' };
      }
      if (!requestData.origin.trim() || !requestData.destination.trim() || requestData.amount <= 0) {
        throw new Error('请完善委托信息');
      }
      const orderData = {
        start_address: requestData.origin.trim(),
        end_address: requestData.destination.trim(),
        item_description: (requestData.description || '').trim(),
        total_amount: Number(requestData.amount),
        order_image: requestData.image || null // **确保传递 image 字段** (文件名或 null)
      };
      const response = await orderAPI.createOrder(orderData);
      if (response.data && response.data.success) {
        await loadOrders();
        return { success: true, message: response.data.message || '发布成功' };
      } else {
        throw new Error(response.data.message || '发布失败');
      }
    } catch (err) {
      console.error('发布订单失败 (Store):', err);
      throw err; 
    }
  }


  async function cancelOrder(orderId) {
    try {
      const response = await orderAPI.cancelOrder(orderId);
      if (response.data && response.data.success) {
        await loadOrders();
      } else {
        throw new Error(response.data.message || '取消订单操作未成功');
      }
    } catch (err) {
      console.error('取消订单失败 (Store):', err);
      throw err; 
    }
  }

  async function reviewOrder(orderId, reviewData) {
    try {
      const response = await orderAPI.reviewOrder(orderId, reviewData);
      if (response.data && response.data.success) {
        await loadOrders();
      } else {
        throw new Error(response.data.message || '评价订单操作未成功');
      }
    } catch (err) {
      console.error('评价订单失败 (Store):', err);
      throw err;
    }
  }

  async function deleteOrder(orderId) {
    try {
      const response = await orderAPI.deleteOrder(orderId);
      if (response.data && response.data.success) {
        await loadOrders();
      } else {
        throw new Error(response.data.message || '删除订单操作未成功');
      }
    } catch (err)
    {
      console.error('删除订单失败 (Store):', err);
      throw err;
    }
  }

  return {
    activeTab,
    orders,
    requests,
    groupedOrders,
    isLoading,
    error,
    loadOrders,
    handleTabChange,
    publishNewOrder,
    addRequest,
    cancelOrder,
    reviewOrder,
    deleteOrder
  }
})