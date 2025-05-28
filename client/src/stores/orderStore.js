import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  createOrder, 
  getMyOrders, 
  getOrderDetail, 
  cancelOrder as apiCancelOrder,
  restoreOrder as apiRestoreOrder,
  reviewOrder as apiReviewOrder,
  uploadOrderImage
} from '@/api/order.js'
// import information from '@/assets/data/information.json'
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
  const error = ref(null);

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
  
  const loadOrders=async()=> {
      loading.value = true
      error.value = null
      try {
        const response = await getMyOrders()
        orders.value = response.data || []
      } catch (error) {
        error.value = error.message
        console.error('加载订单失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 新增：提交订单（将草稿转为正式订单）
    const submitOrders=async()=> {
      loading.value = true
      error.value = null
      
      try {
        const submittedOrders = []
        
        for (const request of this.requests) {
          // 构造后端期望的数据格式
          const orderData = {
            start_address: request.origin,
            end_address: request.destination,
            item_description: request.description,
            pickup_code: request.orderInfo.pickupCode || '',
            locker_number: request.orderInfo.lockerNumber || '',
            total_amount: request.amount,
            coupon_discount: 0, // 后续可以从 request 中获取
            image_url: request.orderInfo.imageUrl || ''
          }
          
          const response = await createOrder(orderData)
          submittedOrders.push(response.data)
        }
        
        // 提交成功后清空草稿
        requests.value = []
        
        // 重新加载订单列表
        await loadOrders()
        
        return submittedOrders
      } catch (error) {
        error.value = error.message
        throw error
      } finally {
        loading.value = false
      }
    }

    // 新增：取消订单
     const cancelOrder=async(orderId)=> {
      try {
        await apiCancelOrder(orderId)
        // 更新本地状态
        const order = orders.value.find(o => o.id === orderId)
        if (order) {
          order.order_status = 'cancelled'
          order.cancelled_at = new Date().toISOString()
        }
      } catch (error) {
        error.value = error.message
        throw error
      }
    }

    // 新增：恢复订单
    const restoreOrder =async(orderId)=> {
      try {
        await apiRestoreOrder(orderId)
        const order = orders.value.find(o => o.id === orderId)
        if (order) {
          order.order_status = 'pending'
          order.cancelled_at = null
        }
      } catch (error) {
        error.value = error.message
        throw error
      }
    }

    // 新增：评价订单
     const reviewOrder=async(orderId, reviewData)=> {
      try {
        await apiReviewOrder(orderId, reviewData)
        const order = orders.value.find(o => o.id === orderId)
        if (order) {
          order.user_rating = reviewData.rating
          order.user_review = reviewData.comment
          order.review_time = new Date().toISOString()
        }
      } catch (error) {
        error.value = error.message
        throw error
      }
    }

    // 新增：上传订单图片
     const uploadImage = async(file)=> {
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await uploadOrderImage(formData)
        return response.data.url
      } catch (error) {
        error.value = error.message
        throw error
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
    error,
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
    uploadImage,
    submitOrders
  }
})
