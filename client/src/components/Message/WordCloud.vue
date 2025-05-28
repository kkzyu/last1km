<template>
  <div class="word-cloud-card">
    <h3 class="card-title">评价词云</h3>
    <div v-if="loading" class="loading-state">
      <a-spin />
    </div>
    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>
    <div v-else-if="processedKeywords && processedKeywords.length > 0" class="word-cloud-container">
      <div v-for="(keyword, index) in processedKeywords" :key="index" 
           class="keyword" 
           :style="getKeywordStyle(keyword)">
        {{ keyword.text }}
      </div>
    </div>
    <div v-else class="empty-state">
      <p>暂无评价数据</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  keywords: {
    type: Array,
    default: () => []
  }
});

const loading = ref(false);
const error = ref(null);

// 处理关键词，为词云显示做准备
const processedKeywords = computed(() => {
  if (!props.keywords || !Array.isArray(props.keywords)) return [];
  
  return props.keywords.map(keyword => {
    // 确保每个关键词对象都有必要的属性
    return {
      text: keyword.text,
      weight: keyword.weight || 1,
      sentiment: keyword.sentiment || 'neutral', // positive, negative, neutral
    };
  }).sort((a, b) => b.weight - a.weight); // 按权重排序
});

// 生成关键词样式
const getKeywordStyle = (keyword) => {
  // 根据权重（使用频率）决定字号
  const minSize = 12;
  const maxSize = 24;
  const fontSize = minSize + (keyword.weight / 10) * (maxSize - minSize);
  
  // 根据情感决定颜色
  let color;
  switch(keyword.sentiment) {
    case 'positive':
      color = '#52c41a'; // 正面评价显示绿色
      break;
    case 'negative':
      color = '#f5222d'; // 负面评价显示红色
      break;
    default:
      color = '#1890ff'; // 中性评价显示蓝色
  }
  
  return {
    fontSize: `${fontSize}px`,
    color,
    fontWeight: keyword.weight > 5 ? 'bold' : 'normal',
    padding: '4px 8px',
    margin: '3px',
    display: 'inline-block',
    borderRadius: '4px',
    backgroundColor: `${color}10` // 添加一点轻微背景色
  };
};

onMounted(() => {
  // 这里可以添加加载动画或其他初始化逻辑
  if (props.keywords && props.keywords.length > 0) {
    loading.value = false;
  }
});
</script>

<style scoped>
.word-cloud-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
  height: 100%;
}

.card-title {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

.word-cloud-container {
  text-align: center;
  padding: 10px;
  min-height: 100px;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px;
  color: #999;
}

.keyword {
  transition: all 0.3s ease;
  cursor: default;
}

.keyword:hover {
  transform: scale(1.1);
}
</style>