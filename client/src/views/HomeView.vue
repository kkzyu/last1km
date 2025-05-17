<template>
  <div class="home-page">
    <header class="top-nav">
      <div class="logo">学士配送</div>
  
    </header>

    <section class="carousel-section">
      <div class="carousel-placeholder">
        <img 
          src="https://via.placeholder.com/800x200" 
          alt="广告位"
          @error="handleImageError"
          v-if="!imageFailed">
        <div v-else class="image-failed">failed</div>
      </div>
    </section>

    <section class="history-orders">
      <div class="section-header">
        <h2>我的历史订单</h2>
        <button class="publish-button" @click="publishNewOrder">发布委托 +</button>
      </div>
      <div class="order-list">
        <template v-for="(group, date) in groupedOrders" :key="date">
          <div 
            v-for="order in group"
            :key="order.id"
            class="order-item"
            :class="{
              'in-progress': order.status === '进行中',
              'cancelled': order.status === '已取消',
              'completed': order.status === '已完成'
            }">

            <div class="order-details">
              <div class="order-status">{{ order.status }}</div>
              <p>订单号：{{ order.id }}</p>
              <p>{{ order.from }} → {{ order.to }}</p>
              <p>速递物品：{{ order.item }}</p>
              <p v-if="order.eta">预计 <span>{{ order.eta }}</span> 分钟后送达</p>
              <p v-else-if="order.description">{{ order.description }}</p>
            </div>
          </div>
        </template>
      </div>
    </section>

    <footer class="bottom-nav">
      <div class="nav-item active">
        <span class="icon">🏠</span> 
        首页
      </div>
      <div class="nav-item">
        <span class="icon">💬</span> 
        <span class="badge">3</span> 
        消息
      </div>
      <div class="nav-item">
        <span class="icon">👤</span> 
        我的
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import information from '@/assets/information.json';

const activeTab = ref('home');
const orders = ref([]);

// 从JSON文件加载订单数据
onMounted(() => {
  orders.value = information.orders;
});

const cancelOrder = (orderId) => {
  console.log('取消订单:', orderId);
};

const reviewOrder = (orderId) => {
  console.log('评价订单:', orderId);
};

const publishNewOrder = () => {
  console.log('发布新委托');
};

const imageFailed = ref(false);
const handleImageError = () => {
  imageFailed.value = true;
};

// 添加计算属性分组订单
const groupedOrders = computed(() => {
  const groups = {};
  orders.value.forEach(order => {
    if (!groups[order.date]) {
      groups[order.date] = [];
    }
    groups[order.date].push(order);
  });
  return groups;
});
</script>

<style scoped>
.home-page {
  font-family: sans-serif;
  display: flex;
  flex-direction: column;
  height: 100vh; /* 假设应用占满整个屏幕高度 */
  background-color: #f4f4f4; /* 页面背景色 */
}

/* 顶部导航栏 */
.top-nav {
  background-color: #2196F3; /* 蓝色背景 */
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}


/* 轮播图 */
.carousel-section {
  /* 根据您的轮播图组件调整样式 */
  height: 200px; /* 示例高度 */
  background-color: #e0e0e0; /* 占位背景色 */
  display: flex;
  justify-content: center;
  align-items: center;
}
.carousel-section img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover; /* 图片填充方式 */
}

/* 历史订单 */

.date-header {
  font-size: 1em;
  color: #666;
  margin: 15px 0 5px;
  padding-left: 10px;
  border-left: 3px solid #2196F3;
}

.history-orders {
  padding: 15px;
  flex: 1;  
  overflow-y: auto; 
  height: 0; 
}
.history-orders .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.history-orders h2 {
  font-size: 1.2em;
  color: #333;
  margin: 0;
}
.history-orders .publish-button {
  background-color: #1976D2; /* 深蓝色按钮 */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1em;
}

.order-list .order-item {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* 垂直顶部对齐 */
}
.order-item .order-date {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 10px;
  writing-mode: vertical-rl; /* 文字竖排，从右到左 */
  text-orientation: mixed;
  padding-right: 15px;
  border-right: 1px solid #eee; /* 分隔线 */
  align-self: stretch; /* 撑开高度 */
  display: flex;
  align-items: center; /* 垂直居中文本 */
}

.order-item .order-details {
  flex-grow: 1;
}
.order-item .order-status {
  font-weight: bold;
  margin-bottom: 8px;
}
.order-item.in-progress .order-status {
  color: #FF9800; /* 橙色 */
}
.order-item.cancelled .order-status {
  color: #9E9E9E; /* 灰色 */
}
.order-item.completed .order-status {
  color: #4CAF50; /* 绿色 */
}
.order-item p {
  font-size: 0.9em;
  color: #333;
  margin: 5px 0;
}
.order-item p span {
  color: #E91E63; /* 红色，用于高亮预计时间 */
  font-weight: bold;
}

.order-item .cancel-button,
.order-item .review-button {
  border: none;
  padding: 8px 12px;
  border-radius: 15px;
  cursor: pointer;
  font-size: 0.9em;
  align-self: center; /* 按钮垂直居中 */
}
.order-item .cancel-button {
  background-color: #f44336; /* 红色 */
  color: white;
}
.order-item .cancel-button:disabled {
  background-color: #bdbdbd;
  cursor: not-allowed;
}
.order-item .review-button {
  background-color: #2196F3; /* 蓝色 */
  color: white;
}

/* 底部导航栏 */
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
  padding: 10px 0;
  position: fixed; /* 固定在底部 */
  bottom: 0;
  left: 0;
  width: 100%;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
}
.bottom-nav .nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 0.8em;
  color: #757575;
  cursor: pointer;
  position: relative; /* 用于定位徽章 */
}
.bottom-nav .nav-item.active {
  color: #1976D2; /* 激活状态的颜色 */
}
.bottom-nav .nav-item .icon {
  font-size: 1.5em; /* 图标大小 */
  margin-bottom: 3px;
}
.bottom-nav .nav-item .badge {
  position: absolute;
  top: -5px;
  right: -8px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 2px 5px;
  font-size: 0.7em;
  font-weight: bold;
}

/* 针对手机屏幕可能需要的一些调整 */
@media (max-width: 768px) {
  .top-nav .logo {
    font-size: 1.2em;
  }
  .history-orders h2 {
    font-size: 1.1em;
  }
  .history-orders .publish-button {
    padding: 8px 12px;
    font-size: 0.9em;
  }
}
.carousel-placeholder {
  height: 200px;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.image-failed {
  color: #666;
  font-size: 1.2em;
}
</style>