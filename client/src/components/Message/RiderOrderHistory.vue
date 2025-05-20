<template>
  <div class="rider-order-history">
    <h3>TA为我送过的单</h3>
    <div v-if="isLoading" class="loading-state">加载历史订单中...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <div v-else-if="orders && orders.length">
      <OrderHistoryItem
        v-for="order in orders"
        :key="order.orderId"
        :order="order"
        @submit-review="handleReviewSubmission"
      />
    </div>
    <div v-else class="empty-state">
      <p>这位送餐员还没有为您送过订单。</p>
    </div>
  </div>
</template>

<script setup>
import OrderHistoryItem from './OrderHistoryItem.vue';

const props = defineProps({
  orders: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['order-reviewed']);

const handleReviewSubmission = (reviewData) => {
  // Emit an event so the parent page can (conceptually) update the main data source
  // For this front-end only example, the OrderHistoryItem updates its own display.
  // If we needed to persist this, the parent would handle the API call.
  console.log('Review submitted in RiderOrderHistory:', reviewData);
  emit('order-reviewed', reviewData);
};
</script>

<style scoped>
.rider-order-history {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}
.rider-order-history h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  font-size: 1.2em;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 20px;
  color: #777;
  font-size: 0.95em;
}
.error-state {
  color: #dc3545;
}
</style>