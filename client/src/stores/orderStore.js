import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { orderAPI } from '@/api/api'

export const useOrderStore = defineStore('order', () => {
  const activeTab = ref('home')
  const orders = ref([])
  const imageFailed = ref(false)
  const requests = ref([]) // 委托请求数组

  const groupedOrders = computed(() => {
    const groups = {}
    orders.value.forEach(order => {
      const date = new Date(order.created_at).toLocaleDateString('zh-CN')
      if (!groups[date]) {
        groups[date] = []
      }
      groups[date].push(order)
    })
    return groups
  })
  async function loadOrders() {
    try {
      const response = await orderAPI.getOrders();
      if (response.data.success) {
        orders.value = response.data.data;
      }
    } catch (error) {
      console.error('加载订单失败:', error);
    }
  }

  function handleTabChange(tab) {
    activeTab.value = tab
  }  function addRequest() {
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
  }async function publishNewOrder(requestData) {
    try {
      if (!requestData.selected) {
        return { success: true, message: '跳过未选中的委托' };
      }

      // 验证必填字段
      if (!requestData.origin.trim() || !requestData.destination.trim() || requestData.amount <= 0) {
        return { success: false, message: '请完善委托信息' };
      }    // 构建请求数据
    const orderData = {
      start_address: requestData.origin.trim(),
      end_address: requestData.destination.trim(),
      item_description: (requestData.description || '').trim(),
      total_amount: Number(requestData.amount)
    };
    try {
      const response = await orderAPI.createOrder(orderData);
      if (response && response.data && response.data.success) {
        await loadOrders(); // 刷新订单列表
        return { success: true, message: '发布成功' };
      }
      return { success: false, message: response?.data?.message || '发布失败' };
    } catch (error) {
      console.error('发布订单失败:', error);
      if (error.response) {
        // 处理特定的错误状态码
        switch (error.response.status) {
          case 401:
            return { success: false, message: '认证失败，请重新登录' };
          case 400:
            return { success: false, message: error.response.data?.message || '请求参数错误' };
          case 500:
            return { success: false, message: '服务器错误，请稍后重试' };
          default:
            return { success: false, message: error.response.data?.message || '发布失败，请重试' };
        }
      }
      // 处理网络错误
      if (error.code === 'ERR_NETWORK') {
        return { success: false, message: '网络连接失败，请检查网络后重试' };
      }
      return { success: false, message: error.message || '发布失败，请重试' };
    }
    } catch (error) {
      console.error('发布订单失败:', error);
      return { success: false, message: '发布失败，请检查网络连接' };
    }
  }

  function handleImageError() {
    imageFailed.value = true
  }

  return {
    activeTab,
    orders,
    imageFailed,
    requests,
    groupedOrders,
    loadOrders,
    handleTabChange,
    publishNewOrder,
    handleImageError,
    addRequest,
  }
})
