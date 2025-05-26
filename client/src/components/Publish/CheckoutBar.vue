<template>
  <div class="checkout-bar-container">
    <div class="checkout-bar-content">
      <div class="left-actions">
        <div class="select-all">
          <a-checkbox v-model:checked="selectAll">全选</a-checkbox>
        </div>
      </div>
      <div class="right-actions">
        <div class="total-amount">
          <span>总计:</span>
          <span class="amount-value">¥{{ formattedTotalAmount }}</span>
        </div>
        <button 
          class="checkout-button"
          :disabled="isCheckoutDisabled"
          @click="handleCheckout"
        >
          提交订单
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useOrderStore } from '@/stores/orderStore';

const router = useRouter();
const orderStore = useOrderStore();

const props = defineProps({
  totalTaskAmount: {
    type: Number,
    default: 0
  },
  onSubmit: {
    type: Function,
    required: true
  }
});

const selectAll = computed({
  get: () => {
    return orderStore.requests.length > 0 && orderStore.requests.every(request => request.selected);
  },
  set: (value) => {
    orderStore.requests.forEach(request => {
      request.selected = value;
    });
  }
});

const formattedTotalAmount = computed(() => {
  return props.totalTaskAmount.toFixed(2);
});

const isCheckoutDisabled = computed(() => {
  return props.totalTaskAmount <= 0 || !orderStore.requests.some(r => r.selected);
});

const handleCheckout = async () => {
  if (isCheckoutDisabled.value) return;
  const success = await props.onSubmit();
  if (success) {
    router.push('/');
  }
};
</script>

<style scoped>
.checkout-bar-container {
  position: absolute;
  bottom: 0px;
  left: 0;
  right: 0;
  z-index: 99;
  display: flex;
  justify-content: center;
}

.checkout-bar-content {
  width: 100%;
  max-width: 390px;
  background-color: #fff;
  padding: 10px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #e9e9e9;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.08);
  height: 60px;
  box-sizing: border-box;
}

.left-actions {
  display: flex;
  align-items: center;
}

.right-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.total-amount {
  font-size: 13px;
  color: #555;
  display: flex;
  align-items: baseline;
}

.amount-value {
  font-size: 17px;
  font-weight: bold;
  color: #FF6347;
  margin-left: 4px;
}

.checkout-button {
  background-color: #007BFF;
  color: white;
  border: none;
  padding: 9px 22px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 18px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.checkout-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.checkout-button:disabled {
  background-color: #a0c7e8;
  cursor: not-allowed;
}
</style>