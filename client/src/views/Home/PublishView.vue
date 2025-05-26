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
  orderStore.requests[index] = { ...newRequest };
};

const handleSubmitOrders = async () => {
  try {
    // 检查登录状态
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert('请先登录');
      router.push('/login');
      return false;
    }
    
    // 验证是否有选中的委托
    const selectedRequests = orderStore.requests.filter(request => request.selected);
    if (selectedRequests.length === 0) {
      alert('请至少选择一个委托');
      return false;
    }

    // 验证所有选中委托的必填字段
    const invalidRequest = selectedRequests.find(request => {
      return !request.origin || !request.destination || request.amount <= 0;
    });

    if (invalidRequest) {
      alert('请完善所有选中委托的信息');
      return false;
    }

    // 发布选中的委托
    const results = await Promise.all(
      selectedRequests.map(request => orderStore.publishNewOrder(request))
    );

    // 检查发布结果
    const failedResults = results.filter(r => !r.success);
    if (failedResults.length === 0) {
      // 全部成功，清空请求列表并返回首页
      orderStore.requests = [];
      return true;
    } else {
      // 部分失败，显示错误信息
      const errors = failedResults.map(r => r.message).join('\n');
      alert(`部分委托发布失败:\n${errors}`);
      // 只移除成功发布的委托
      const successIndices = results.map((r, i) => r.success ? i : -1).filter(i => i !== -1);
      orderStore.requests = orderStore.requests.filter((_, i) => !successIndices.includes(i));
      return false;
    }
  } catch (error) {
    console.error('提交订单失败:', error);
    alert('提交订单失败，请重试');
    return false;
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