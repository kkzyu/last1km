<template>
  <div class="create-request-view">
    <HomeHead />
    <div class="view-header">
      <AddRequestButton @click="handleNewRequest" />
    </div>

    <div class="form-content-wrapper">      <template v-if="orderStore.requests.length > 0">
        <div 
          v-for="(request, index) in orderStore.requests" 
          :key="index"
          class="request-item-container"
        >
          <RequestDetailsForm
            :index="index"
            :request="request"
            @update:request="updateRequest(index, $event)"
          />
        </div>
      </template>
      <div v-else class="empty-state">
        点击上方按钮添加委托
      </div>
    </div>

    <CheckoutBar 
      :total-task-amount="totalAmount"
      :on-submit="handleSubmitOrders"
    />
    <BottomNav />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useOrderStore } from '@/stores/orderStore';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import AddRequestButton from '@/components/Publish/AddRequestButton.vue';
import RequestDetailsForm from '@/components/Publish/RequestDetailsForm.vue';
import CheckoutBar from '@/components/Publish/CheckoutBar.vue';
import HomeHead from '@/components/Header/HomeHead.vue';
import BottomNav from '@/components/Bottom/BottomNav.vue';

const router = useRouter();
const orderStore = useOrderStore();

onMounted(() => {
  if (orderStore.requests.length === 0) {
    handleNewRequest();
  }
});

const totalAmount = computed(() => {
  return orderStore.requests.reduce((sum, request) => {
    if (!request.selected) return sum;
    const amount = parseFloat(request.amount);
    return sum + (isNaN(amount) ? 0 : amount);
  }, 0);
});

const handleNewRequest = () => {
  orderStore.addRequest();
};

const handleRemoveRequest = (index) => {
  orderStore.requests.splice(index, 1);
};

const updateRequest = (index, newRequest) => {
  console.log(`PublishView - 更新委托 ${index + 1}:`, newRequest);
  
  // 确保数组索引有效
  if (index >= 0 && index < orderStore.requests.length) {
    // 直接替换整个对象，而不是合并
    orderStore.requests[index] = newRequest;
    
    console.log(`PublishView - 委托 ${index + 1} 更新后:`, orderStore.requests[index]);
    
    // 验证关键字段
    console.log(`PublishView - 验证字段:`, {
      origin: orderStore.requests[index].origin,
      destination: orderStore.requests[index].destination,
      amount: orderStore.requests[index].amount
    });
  }
};

// 验证单个委托是否完整
const validateRequest = (request, index) => {
  console.log(`验证委托 ${index + 1} - 完整对象:`, request);
  console.log(`验证委托 ${index + 1} - 关键字段:`, {
    origin: request.origin,
    originType: typeof request.origin,
    originLength: request.origin?.length,
    destination: request.destination,
    destinationType: typeof request.destination,
    destinationLength: request.destination?.length,
    amount: request.amount,
    amountType: typeof request.amount,
    description: request.description,
    descriptionType: typeof request.description,
    descriptionIsArray: Array.isArray(request.description)
  });
  
  const errors = [];
  
  
  if (!request.origin || typeof request.origin !== 'string' || !request.origin.trim()) {
    console.log(`委托 ${index + 1} 起点地址验证失败:`, {
      value: request.origin,
      type: typeof request.origin,
      trimmed: request.origin?.trim?.()
    });
    errors.push('起点地址');
  }
  
  if (!request.destination || typeof request.destination !== 'string' || !request.destination.trim()) {
    console.log(`委托 ${index + 1} 终点地址验证失败:`, {
      value: request.destination,
      type: typeof request.destination,
      trimmed: request.destination?.trim?.()
    });
    errors.push('终点地址');
  }
  
  const amount = parseFloat(request.amount);
  if (isNaN(amount) || amount <= 0) {
    console.log(`委托 ${index + 1} 金额验证失败:`, {
      original: request.amount,
      parsed: amount,
      isNaN: isNaN(amount)
    });
    errors.push('委托金额');
  }
  
  // 建议填写但不强制的字段
  const suggestions = [];
  if (!request.originDetail || typeof request.originDetail !== 'string' || !request.originDetail.trim()) {
    suggestions.push('起点具体位置');
  }
  
  if (!request.destinationDetail || typeof request.destinationDetail !== 'string' || !request.destinationDetail.trim()) {
    suggestions.push('终点具体位置');
  }
  
  // 修复 description 的验证
  const description = Array.isArray(request.description) 
    ? request.description.join(' ') 
    : (request.description || '');
  
  if (!description || typeof description !== 'string' || !description.trim()) {
    suggestions.push('物品描述');
  }
  
  // 修复 orderInfo 的验证
  const orderInfo = Array.isArray(request.orderInfo) 
    ? request.orderInfo.join(' ') 
    : (request.orderInfo || '');
    
  if (!orderInfo || typeof orderInfo !== 'string' || !orderInfo.trim()) {
    suggestions.push('取件信息');
  }
  
  if (!request.image) {
    suggestions.push('订单截图');
  }
  
  const result = {
    isValid: errors.length === 0,
    errors,
    suggestions
  };
  
  console.log(`委托 ${index + 1} 验证结果:`, result);
  return result;
};

const handleSubmitOrders = async () => {
  let closeLoadingMessage = null;
  try {
    // 检查登录状态
    const token = localStorage.getItem('token');
    if (!token) {
      message.error('请先登录');
      router.push('/login');
      return false;
    }
    
    // 验证是否有选中的委托
    const selectedRequests = orderStore.requests.filter(request => request.selected);
    if (selectedRequests.length === 0) {
      message.warning('请至少选择一个委托');
      return false;
    }

    console.log('提交前的所有委托数据:', orderStore.requests); // 添加调试日志
    console.log('选中的委托:', selectedRequests); // 添加调试日志

    // 验证所有选中委托的必填字段
    const validationResults = selectedRequests.map((request, selectedIndex) => {
      const originalIndex = orderStore.requests.indexOf(request);
      const result = {
        index: originalIndex + 1,
        selectedIndex,
        ...validateRequest(request, originalIndex)
      };
      console.log(`委托 ${result.index} 验证结果:`, result); // 添加调试日志
      return result;
    });

    // 检查是否有验证失败的委托
    const invalidRequests = validationResults.filter(result => !result.isValid);
    
    if (invalidRequests.length > 0) {
      const errorMessages = invalidRequests.map(result => 
        `委托${result.index}: 缺少 ${result.errors.join('、')}`
      ).join('\n');
      
      console.error('验证失败的委托:', invalidRequests); // 添加调试日志
      message.error(`请完善以下必填信息:\n${errorMessages}`);
      return false;
    }

    // 检查建议填写的字段
    const incompleteRequests = validationResults.filter(result => 
      result.suggestions.length > 0
    );
    
    if (incompleteRequests.length > 0) {
      const suggestionMessages = incompleteRequests.map(result => 
        `委托${result.index}: 建议填写 ${result.suggestions.join('、')}`
      ).join('\n');
      
      // 显示确认对话框
      const confirmed = await new Promise((resolve) => {
        const modal = message.warning({
          content: `以下信息未填写完整，建议补充以提高接单率:\n\n${suggestionMessages}\n\n是否继续发布?`,
          okText: '继续发布',
          cancelText: '去完善',
          onOk: () => {
            modal.destroy();
            resolve(true);
          },
          onCancel: () => {
            modal.destroy();
            resolve(false);
          }
        });
      });
      
      if (!confirmed) {
        return false;
      }
    }

    // 显示loading
    closeLoadingMessage = message.loading('正在发布委托...', 0);

    // 发布选中的委托
    const results = await Promise.all(
      selectedRequests.map(request => orderStore.publishNewOrder(request))
    );

    // 检查发布结果
    const failedResults = results.filter(r => !r.success);
    const successCount = results.length - failedResults.length;

    if (failedResults.length === 0) {
      // 全部成功
      if (closeLoadingMessage) closeLoadingMessage();
      message.success(`成功发布 ${successCount} 个委托！`);
      orderStore.requests = [];
      router.push('/orders'); 
      return true;
    } else {
      // 部分失败或全部失败
      if (closeLoadingMessage) closeLoadingMessage();
      const errors = failedResults.map((r, index) =>
        `委托${index + 1}: ${r.message}`
      ).join('\\n');

      if (successCount > 0) {
        message.warning(`${successCount} 个委托发布成功，${failedResults.length} 个失败:\\n${errors}`);
        const successIndices = results.map((r, i) => r.success ? i : -1).filter(i => i !== -1);
        orderStore.requests = orderStore.requests.filter((_, i) => !successIndices.includes(i));
      } else {
        message.error(`所有委托发布失败:\\n${errors}`);
      }
      return false;
    }
  } catch (error) {
    if (closeLoadingMessage) closeLoadingMessage();
    console.error('提交订单失败:', error);
    message.error(`提交订单失败: ${error.message || '请重试'}`);
    return false;
  }
};

const deleteOrder = async (orderId) => {
  try {
    await orderStore.deleteOrder(orderId);
    message.success('订单已删除');
  } catch (error) {
    message.error('删除订单失败');
  }
};
</script>

<style scoped>
.create-request-view {
  display: flex;
  flex-direction: column;
  background-color: #f4f6f8;
  width: 100%;
  height: 100vh;
  margin: 0 auto;
  position: relative;
}

.view-header {
  padding: 15px;
  background-color: #fff;
  display: flex;
  justify-content: flex-end;
}

.form-content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px 15px 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding-bottom: 75px;
}

.form-content-wrapper::-webkit-scrollbar {
  display: none;
}

.request-item-container {
  margin-bottom: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.request-item-container:last-child {
  margin-bottom: 0;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #777;
  font-size: 16px;
}
</style>