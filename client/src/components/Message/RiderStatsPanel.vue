<template>
  <div class="rider-stats-panel-card">
    <!-- <h3>数据看板</h3> -->
    <div class="stats-grid">
      <div class="stat-item">
        <span class="stat-value">{{ (stats.onTimeRate * 100).toFixed(0) }}%</span>
        <span class="stat-label">准时率</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ (stats.positiveFeedbackRate * 100).toFixed(0) }}%</span>
        <span class="stat-label">好评率</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">{{ stats.averageDailyOrders }}</span>
        <span class="stat-label">日均送单</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="like-icon"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
          {{ stats.likeCount }}
        </span>
        <span class="stat-label">点赞数</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true,
    default: () => ({
      onTimeRate: 0,
      positiveFeedbackRate: 0,
      averageDailyOrders: 0,
      likeCount: 0
    })
  }
});
</script>

<style scoped>
.rider-stats-panel-card {
  background-color: #f9f9f9; /* Slightly different background */
  padding: 15px;
  border-radius: 8px;
  /* box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06); */ /* Optional shadow */
}
/* .rider-stats-panel-card h3 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #333;
  font-size: 1.1em;
  text-align: center;
} */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 columns */
  gap: 12px;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 10px 5px;
  /* background-color: #fff; */ /* Can remove if card has bg */
  border-radius: 6px;
}
.stat-value {
  font-size: 1.25em;
  font-weight: bold;
  color: #007bff;
  margin-bottom: 3px;
  display: flex;
  align-items: center;
}
.stat-value .like-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
  color: #ff4500;
}
.stat-label {
  font-size: 0.75em;
  color: #555;
}
</style>