<template>
    <div class="create-request-view">
        <AddRequestButton @add-request-clicked="handleNewRequest" />
        
        <div class="form-content-wrapper">
          
            <!-- 循环渲染多个委托表单 -->
            <div v-for="(request, index) in orderStore.requests" 
                 :key="request.id" 
                 class="request-item">
                <RequestDetailsForm 
                    :index="index"
                    v-model:origin="request.origin"
                    v-model:destination="request.destination"
                    v-model:description="request.description"
                    v-model:orderInfo="request.orderInfo"
                    v-model:taskAmount="request.amount"
                    @update:taskAmount="updateTotalAmount"
                />
            </div>
        </div> 
        <CheckoutBar :taskAmountFromForm="totalAmount" />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useOrderStore } from '@/stores/orderStore';
import AddRequestButton from '@/components/AddRequestButton.vue'; 
import RequestDetailsForm from '@/components/RequestDetailsForm.vue'; 
import CheckoutBar from '@/components/CheckoutBar.vue';

const orderStore = useOrderStore();
const currentTaskAmount = ref(null);

// 确保页面加载时至少有一个委托表单
if (orderStore.requests.length === 0) {
    orderStore.addRequest();
}

// 计算所有委托的总金额
const totalAmount = computed(() => {
    return orderStore.requests.reduce((sum, request) => {
        return sum + (Number(request.amount) || 0);
    }, 0);
});

const handleNewRequest = () => {
    console.log('点击前的请求数量：', orderStore.requests.length);
    orderStore.addRequest();
    console.log('点击后的请求数量：', orderStore.requests.length);
};

const updateTotalAmount = () => {
    console.log('更新总金额为:', totalAmount.value);
};
</script>

<style scoped>
.create-request-view {
    background-color: #fff;
    /* 修改高度和滚动设置 */
    height: calc(100vh - 180px); /* 减去底部导航栏高度 */
    overflow-y: auto;
    position: relative;
    padding-bottom: 20px; /* 为底部结算栏留出空间 */
}

.form-content-wrapper {
    padding: 0 15px; 
    margin-bottom: 20px;
}

.request-item {
    margin-bottom: 20px;
    border-radius: 8px;
    background-color: #fff;
}

/* 修改结算栏样式确保固定在底部 */
.create-request-view > :deep(.checkout-bar) {
    position: fixed;
    bottom: 65px;
    left: 0;
    width: 100%;
    z-index: 10;
    background-color: #fff;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

/* 添加滚动优化 */
@media (hover: none) {
    .create-request-view {
        -webkit-overflow-scrolling: touch;
    }
}
</style>