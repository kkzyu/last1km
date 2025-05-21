<template>
  <div class="checkout-bar-container"> 
    <div class="checkout-bar-content">
      <div class="left-actions">
        <div class="select-all">
          <input type="checkbox" id="select-all-checkbox" v-model="selectAll" class="custom-checkbox">
          <label for="select-all-checkbox">全选</label>
        </div>
        <div class="coupon-select" @click="handleCouponSelect">
          <span>选择卡券</span>
          <span class="coupon-arrow">
              <svg width="12" height="7" viewBox="0 0 12 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 1L6 6L11 1" stroke="#E63C3C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
          </span>
        </div>
      </div>
      <div class="right-actions">
        <div class="total-amount">
          共计: <span class="amount-value">{{ formattedTotalAmount }}元</span>
        </div>
        <button class="checkout-button" @click="handleCheckout" :disabled="isCheckoutDisabled">结算</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useOrderStore } from '@/stores/orderStore' // Assuming this store has selectedOrders and totalAmount for checkout

const props = defineProps({
  totalTaskAmount: { // Renamed from taskAmountFromForm for clarity
    type: Number,
    default: 0
  }
})

const orderStore = useOrderStore() // This might be for selected items, not the total from forms

// This selectAll likely refers to items in a cart or list, not the forms themselves.
// If it's for the forms, the logic needs to be in the parent.
const selectAll = computed({
  get: () => orderStore.requests.length > 0 && orderStore.requests.every(r => r.selected), // Example if forms can be selected
  // get: () => orderStore.orders.length > 0 && orderStore.orders.length === orderStore.selectedOrders.length, // Original logic
  set: (value) => {
    // orderStore.toggleSelectAllRequests(value) // Example
    orderStore.toggleSelectAll(value) // Original logic
  }
})

// The formattedTotalAmount should probably use the prop passed from the parent,
// which is the sum of amounts from the RequestDetailsForm instances.
const formattedTotalAmount = computed(() => {
  return props.totalTaskAmount.toFixed(2)
  // return orderStore.totalAmount.toFixed(2) // Original: This might be a different total from the store
})

const isCheckoutDisabled = computed(() => {
  return props.totalTaskAmount <= 0; // Disable if nothing to checkout
  // Or based on selected items: return orderStore.selectedOrders.length === 0;
});

const handleCouponSelect = () => {
  console.log('Select coupon clicked');
  // Implement coupon selection logic
}

const handleCheckout = () => {
  if (isCheckoutDisabled.value) return;
  console.log('Checkout clicked with total:', props.totalTaskAmount);
  // Implement checkout logic
}
</script>

<style scoped>
.checkout-bar-container {
  position: fixed;
  /* Assuming global BottomNav is ~60px. CheckoutBar sits above it. */
  /* If no global BottomNav, use bottom: 0; */
  bottom: 0px; /* Adjust to actual BottomNav height */
  left: 0;
  right: 0;
  z-index: 1000; /* Ensure it's above other content but potentially below modals */
  display: flex; /* To center the content if max-width is used */
  justify-content: center; /* To center the content if max-width is used */
}

.checkout-bar-content {
  width: 100%;
  max-width: 390px; /* Match parent's max-width */
  background-color: #fff;
  padding: 10px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #e9e9e9;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.08);
  height: 60px; /* Fixed height for the bar */
  box-sizing: border-box;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.select-all {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
}

.select-all label {
  margin-left: 6px;
  cursor: pointer;
}

/* Using native checkbox and styling it slightly */
.custom-checkbox {
  appearance: none;
  -webkit-appearance: none;
  background-color: #fff;
  border: 1.5px solid #ccc;
  border-radius: 4px;
  width: 18px;
  height: 18px;
  cursor: pointer;
  position: relative;
  outline: none;
}

.custom-checkbox:checked {
  background-color: #007bff;
  border-color: #007bff;
}

.custom-checkbox:checked::after {
  content: '✔';
  font-size: 12px;
  color: white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}


.coupon-select {
  font-size: 14px;
  color: #E63C3C;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: 500;
}
.coupon-arrow {
  margin-left: 4px;
  display: flex;
  align-items: center;
}
.coupon-arrow svg path {
    stroke: #E63C3C;
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
.total-amount .amount-value {
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
  background-color: #a0c7e8; /* Lighter blue for disabled state */
  cursor: not-allowed;
}
</style>