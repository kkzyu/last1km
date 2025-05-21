<template>
  <div class="order-history-item-card">
    <div class="order-header">
      <h4>订单号: {{ order.orderId }}</h4>
      <span>{{ formatDate(order.date) }}</span>
    </div>
    <p><strong>商品:</strong> {{ order.items.join(', ') }}</p>
    <p><strong>金额:</strong> ¥{{ order.totalAmount.toFixed(2) }}</p>

    <div class="review-section">
      <h5>评价此订单</h5>
      <div v-if="!submittedReview && !order.userReview">
        <div class="rating-stars">
          <span
            v-for="star in 5"
            :key="star"
            @click="setRating(star)"
            :class="{ 'filled': star <= currentRating, 'interactive': !submittedReview }"
          >
            ★
          </span>
        </div>
        <textarea
          v-model="currentComment"
          placeholder="写下您的评价 (可选)"
          rows="3"
          :disabled="submittedReview"
        ></textarea>
        <button @click="submitReview" :disabled="currentRating === 0 || submitting">
          {{ submitting ? '提交中...' : '提交评价' }}
        </button>
      </div>
      <div v-else-if="currentLocalReview" class="existing-review">
        <p><strong>您的评分:</strong>
          <span class="rating-stars static">
            <span v-for="star in 5" :key="star" :class="{ 'filled': star <= currentLocalReview.rating }">★</span>
          </span>
        </p>
        <p><strong>您的评价:</strong> {{ currentLocalReview.comment || '无' }}</p>
      </div>
      <div v-else class="no-review-placeholder">
         <p>您尚未评价此订单。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['submit-review']);

const currentRating = ref(0);
const currentComment = ref('');
const submittedReview = ref(false);
const submitting = ref(false);
const currentLocalReview = ref(null); // To hold the review data once submitted or loaded

onMounted(() => {
  if (props.order.userReview) {
    currentLocalReview.value = { ...props.order.userReview };
    currentRating.value = props.order.userReview.rating;
    currentComment.value = props.order.userReview.comment;
    submittedReview.value = true;
  }
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('zh-CN', options);
};

const setRating = (rating) => {
  if (!submittedReview.value) {
    currentRating.value = rating;
  }
};

const submitReview = () => {
  if (currentRating.value === 0 || submitting.value) return;
  submitting.value = true;
  // Simulate API call
  setTimeout(() => {
    const reviewData = {
      rating: currentRating.value,
      comment: currentComment.value.trim()
    };
    emit('submit-review', { orderId: props.order.orderId, review: reviewData });
    currentLocalReview.value = reviewData; // Update local display
    submittedReview.value = true;
    submitting.value = false;
  }, 500);
};
</script>

<style scoped>
.order-history-item-card {
  background-color: #fff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.07);
  margin-bottom: 50px;
}
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #eee;
}
.order-header h4 {
  margin: 0;
  font-size: 1.1em;
  color: #333;
}
.order-header span {
  font-size: 0.8em;
  color: #777;
}
.order-history-item-card p {
  font-size: 0.9em;
  color: #555;
  margin: 5px 0;
  /* margin-bottom: 40px; */
}
.review-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}
.review-section h5 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1em;
  color: #444;
}
.rating-stars span {
  font-size: 1.8em;
  color: #ccc;
}
.rating-stars span.interactive {
   cursor: pointer;
}
.rating-stars span.filled {
  color: #ffc107;
}
.rating-stars.static span {
   font-size: 1.1em; /* Smaller for display */
}
textarea {
  width: calc(100% - 20px);
  padding: 8px 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9em;
  resize: vertical;
}
.review-section button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
}
.review-section button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.review-section button:hover:not(:disabled) {
  background-color: #218838;
}
.existing-review p {
  margin: 5px 0;
}
.no-review-placeholder p {
  color: #888;
  font-style: italic;
}
</style>