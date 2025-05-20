<template>
  <div class="word-cloud-square-card">
    <h4>评价词云</h4>
    <div v-if="keywords && keywords.length" class="keywords-container">
      <span
        v-for="keyword in sortedKeywords"
        :key="keyword.text"
        class="keyword-tag"
        :class="getSentimentClass(keyword.sentiment)"
        :style="getKeywordStyle(keyword.weight)"
      >
        {{ keyword.text }}
      </span>
    </div>
    <p v-else class="no-keywords">暂无评价关键词</p>
  </div>
</template>

<script setup>
// ... (script remains the same as in the previous response for WordCloud.vue)
import { computed } from 'vue';

const props = defineProps({
  keywords: {
    type: Array,
    required: true,
    default: () => []
  }
});

const sortedKeywords = computed(() => {
  return [...props.keywords].sort((a, b) => b.weight - a.weight);
});

const getKeywordStyle = (weight) => {
  const minFontSize = 0.75; // em, adjusted for potentially smaller container
  const maxFontSize = 1.6; // em
  const maxWeight = Math.max(...props.keywords.map(k => k.weight).filter(Number.isFinite), 5);
  const minWeight = Math.min(...props.keywords.map(k => k.weight).filter(Number.isFinite), 1);

  let fontSize = minFontSize;
  if (maxWeight > minWeight) {
    fontSize = minFontSize + ((weight - minWeight) / (maxWeight - minWeight)) * (maxFontSize - minFontSize);
  } else if (props.keywords.length > 0) {
    fontSize = (minFontSize + maxFontSize) / 2;
  }
  return {
    fontSize: `${Math.max(minFontSize, Math.min(maxFontSize, fontSize))}em`,
  };
};

const getSentimentClass = (sentiment) => {
  if (sentiment === 'positive') return 'sentiment-positive';
  if (sentiment === 'negative') return 'sentiment-negative';
  return 'sentiment-neutral';
};
</script>

<style scoped>
.word-cloud-square-card {
  background-color: #fff;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  /* To make it square-ish, we can use aspect-ratio or set fixed height/width */
  /* For a dynamic square based on width: */
  width: 100%; /* Take available width in its column */
  aspect-ratio: 1 / 1; /* Make it a square */
  overflow: hidden; /* Hide overflow if content is too much for square */
}
.word-cloud-square-card h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.1em;
  text-align: center;
  flex-shrink: 0; /* Prevent title from shrinking */
}
.keywords-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 10px;
  justify-content: center;
  align-items: center;
  flex-grow: 1; /* Allow this to take remaining space */
  overflow-y: auto; /* Allow scrolling within the keyword area if needed */
  padding: 5px; /* Small padding inside */
}
.keyword-tag {
  padding: 5px 10px;
  border-radius: 15px;
  font-weight: 500;
  line-height: 1;
  transition: transform 0.2s ease-in-out;
  cursor: default;
}
.keyword-tag:hover {
    transform: scale(1.05); /* Slightly less aggressive hover */
}
.sentiment-positive { background-color: #e6ffed; color: #28a745; border: 1px solid #b7eac9; }
.sentiment-negative { background-color: #ffebee; color: #dc3545; border: 1px solid #f8c6c7; }
.sentiment-neutral { background-color: #f0f0f0; color: #555; border: 1px solid #dcdcdc; }
.no-keywords {
  text-align: center;
  color: #777;
  margin: auto; /* Center vertically and horizontally */
  font-size: 0.9em;
}
</style>