import { defineStore } from 'pinia';
import { orderAPI } from '@/api/api';

export const useOrderStore = defineStore('order', {
  state: () => ({
    requests: [],
    orders: [],
    loading: false
  }),

  getters: {
    groupedOrders: (state) => {
      if (!state.orders || state.orders.length === 0) {
        return {};
      }

      const grouped = {};
      state.orders.forEach(order => {
        const date = formatOrderDate(order.created_at);
        if (!grouped[date]) {
          grouped[date] = [];
        }
        grouped[date].push(order);
      });

      const sortedKeys = Object.keys(grouped).sort((a, b) => new Date(b) - new Date(a));
      const sortedGrouped = {};
      sortedKeys.forEach(key => {
        sortedGrouped[key] = grouped[key];
      });

      return sortedGrouped;
    }
  },

  actions: {
    addRequest() {
      const newRequest = {
        origin: '',
        destination: '',
        originDetail: '',           
        destinationDetail: '',      
        description: '',            
        orderInfo: '',              
        amount: 0,
        selected: true,
        image: null,
        originLocation: null,       
        destinationLocation: null,  
        estimatedTime: null,        
        createdAt: new Date().toISOString()
      };
      this.requests.push(newRequest);
    },

    async loadOrders() {
      return this.fetchOrders();
    },

    async fetchOrders() {
      try {
        this.loading = true;
        const response = await orderAPI.getOrders();
        
        if (response.data && response.data.success) {
          this.orders = response.data.data || [];
        } else {
          console.error('获取订单失败:', response.data?.message);
          this.orders = [];
        }
      } catch (error) {
        console.error('获取订单失败:', error);
        this.orders = [];
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // 使用后端API期望的确切字段名
    async publishNewOrder(requestData) {
      try {
        this.loading = true;
        
        // 清理和验证数据
        const cleanDescription = Array.isArray(requestData.description) 
          ? requestData.description.join(' ') 
          : String(requestData.description || '');
          
        const cleanOrderInfo = Array.isArray(requestData.orderInfo) 
          ? requestData.orderInfo.join(' ') 
          : String(requestData.orderInfo || '');
        
        console.log('清理前数据:', {
          origin: requestData.origin,
          destination: requestData.destination,
          description: requestData.description,
          orderInfo: requestData.orderInfo,
          amount: requestData.amount
        });
        
        // 构建订单数据 - 使用后端API期望的确切字段名
        const orderData = {
          // 地址信息 - 使用API期望的字段名
          origin: String(requestData.origin || '').trim(),
          destination: String(requestData.destination || '').trim(),
          origin_detail: String(requestData.originDetail || '').trim(),
          destination_detail: String(requestData.destinationDetail || '').trim(),
          
          // 订单信息 - 使用API期望的字段名
          description: cleanDescription.trim(),
          order_info: cleanOrderInfo.trim(),
          
          // 金额信息 - 使用API期望的字段名
          amount: parseFloat(requestData.amount) || 0,
          
          // 图片 - 使用API期望的字段名
          image: requestData.image || null,
          
          // 位置信息
          origin_lat: requestData.originLocation?.lat || null,
          origin_lng: requestData.originLocation?.lng || null,
          dest_lat: requestData.destinationLocation?.lat || null,
          dest_lng: requestData.destinationLocation?.lng || null,
          
          // 预计配送信息
          estimated_duration: requestData.estimatedTime?.duration || null,
          estimated_distance: requestData.estimatedTime?.distance || null
        };

        console.log('发布订单数据 (API字段映射):', orderData);
        
        // 验证必填字段 - 使用API期望的字段名
        if (!orderData.origin || !orderData.destination) {
          const missingFields = [];
          if (!orderData.origin) missingFields.push('起点地址');
          if (!orderData.destination) missingFields.push('终点地址');
          throw new Error(`请填写必填字段: ${missingFields.join(', ')}`);
        }
        
        if (!orderData.amount || orderData.amount <= 0) {
          throw new Error('请填写有效的委托金额');
        }
        
        const response = await orderAPI.createOrder([orderData]);
        
        if (response.data && response.data.success) {
          await this.fetchOrders();
          return { success: true, data: response.data.data };
        } else {
          return { 
            success: false, 
            message: response.data?.message || '发布失败' 
          };
        }
      } catch (error) {
        console.error('发布订单失败:', error);
        return { 
          success: false, 
          message: error.response?.data?.message || error.message || '网络错误' 
        };
      } finally {
        this.loading = false;
      }
    },

    async cancelOrder(orderId) {
      try {
        const response = await orderAPI.cancelOrder(orderId);
        if (response.data && response.data.success) {
          // 重新获取订单列表以更新状态
          await this.fetchOrders();
          return true;
        }
        return false;
      } catch (error) {
        console.error('取消订单失败:', error);
        throw error;
      }
    },

    async reviewOrder(orderId, reviewData) {
      try {
        const response = await orderAPI.reviewOrder(orderId, reviewData);
        if (response.data && response.data.success) {
          // 重新获取订单列表以更新状态
          await this.fetchOrders();
          return true;
        }
        return false;
      } catch (error) {
        console.error('评价订单失败:', error);
        throw error;
      }
    },

    async deleteOrder(orderId) {
      try {
        const response = await orderAPI.deleteOrder(orderId);
        if (response.data && response.data.success) {
          this.orders = this.orders.filter(order => order.id !== orderId);
          return true;
        }
        return false;
      } catch (error) {
        console.error('删除订单失败:', error);
        throw error;
      }
    },

    clearRequests() {
      this.requests = [];
    }
  }
});

function formatOrderDate(dateString) {
  if (!dateString) return '未知日期';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return '未知日期';
    }
    
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    
    const orderDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const todayDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const yesterdayDate = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate());
    
    if (orderDate.getTime() === todayDate.getTime()) {
      return '今天';
    } else if (orderDate.getTime() === yesterdayDate.getTime()) {
      return '昨天';
    } else {
      return date.toLocaleDateString('zh-CN', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    }
  } catch (error) {
    console.error('日期格式化失败:', error);
    return '未知日期';
  }
}