<template>
  <div class="rider-profile-page">
    <header class="profile-page-header">
      <button @click="goBack" class="back-button" aria-label="返回">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <h4 class="page-title">{{ rider?.name || '送餐员主页' }}</h4>
      <div class="header-placeholder"></div>
    </header>

    <div v-if="isLoading" class="loading-indicator">正在加载送餐员信息...</div>
    <div v-else-if="error" class="error-message">错误: {{ error }}</div>

    <div v-else-if="rider" class="profile-content-scrollable">
      <div class="profile-main-layout">
        <!-- Left Column -->
        <div class="left-column">
          <RiderInfoCard :rider="rider" />
          <WordCloud v-if="rider.stats && rider.stats.reviewKeywords" :keywords="rider.stats.reviewKeywords" />
        </div>

        <!-- Right Column -->
        <div class="right-column">
          <RiderStatsPanel :stats="rider.stats" />
        </div>
      </div>

      <!-- Order History (Full Width Below) -->
      <RiderOrderHistory :orders="riderOrderHistory" :is-loading="isOrdersLoading" :error="ordersError"
        @order-reviewed="handleOrderReviewed" />
    </div>
    <div v-else class="not-found">未找到送餐员信息。</div>

    <footer v-if="rider" class="profile-actions">
      <!-- Footer buttons remain the same -->
      <button @click="blockRider" class="action-button block">拉黑</button>
      <button @click="contactRider" class="action-button contact">联系</button>
      <button @click="likeRider" class="action-button like" :class="{ 'liked': isLikedByCurrentUser }">点赞</button>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { riderAPI } from '@/api/api.js';
// Import the new/renamed components
import RiderInfoCard from '@/components/Message/RiderInfoCard.vue';
import RiderStatsPanel from '@/components/Message/RiderStatsPanel.vue';
import WordCloud from '@/components/Message/WordCloud.vue';
import RiderOrderHistory from '@/components/Message/RiderOrderHistory.vue';

// ... (rest of the script remains largely the same as your last version)
// Ensure fetchRiderData, fetchRiderOrderHistory, and event handlers are present.

const route = useRoute();
const router = useRouter();

const rider = ref(null);
const isLoading = ref(true);
const error = ref(null);

const riderOrderHistory = ref([]);
const isOrdersLoading = ref(true);
const ordersError = ref(null);

const isLikedByCurrentUser = ref(false);
const BASE_URL = import.meta.env.BASE_URL;

const CURRENT_USER_ID = 'user_abc';
const riderId = computed(() => route.params.riderId || 'rider_1');

const resolveAssetPath = (relativePath) => {
  if (!relativePath) return undefined;
  // Ensure no double slashes if relativePath starts with '/' and BASE_URL ends with '/'
  let path = relativePath;
  if (BASE_URL.endsWith('/') && path.startsWith('/')) {
    path = path.substring(1);
  } else if (!BASE_URL.endsWith('/') && !path.startsWith('/')) {
    // This case is unlikely if BASE_URL is like '/last1km/' and path is like 'images/foo.jpg'
    // but good to be mindful. For your JSON paths like "/images/avatar.jpg",
    // the first condition (substring(1)) is what we need.
    // If json path was "images/avatar.jpg", then direct concatenation is fine.
  }
  return `${BASE_URL}${path}`;
};

async function fetchRiderData() {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await riderAPI.getRiderDetails(riderId.value);
    const riderDataFromServer = response.data?.data; // API响应结构

    if (riderDataFromServer) {
      rider.value = {
        ...riderDataFromServer,
        // Resolve the avatar path here
        avatar: riderDataFromServer.avatar ? resolveAssetPath(riderDataFromServer.avatar) : undefined
      };
      // Initialize stats if not present
      if (!rider.value.stats) rider.value.stats = { likeCount: 0, reviewKeywords: [] };
      if (!rider.value.stats.reviewKeywords) rider.value.stats.reviewKeywords = [];
      
      isLikedByCurrentUser.value = localStorage.getItem(`liked_rider_${riderId.value}`) === 'true';
    } else {
      throw new Error(`Rider with ID ${riderId.value} not found`);
    }
  } catch (e) {
    console.error("Failed to fetch rider data:", e);
    error.value = e.message;
    rider.value = null;
  } finally {
    isLoading.value = false;
  }
}

async function fetchRiderOrderHistory() {
  if (!rider.value) return;
  isOrdersLoading.value = true;
  ordersError.value = null;
  try {
    const response = await riderAPI.getRiderOrderHistory(riderId.value);
    const orders = response.data?.data || []; // API响应结构
    riderOrderHistory.value = orders.map(order => ({
      ...order,
      userReview: order.userReview || null
    }));
  } catch (e) {
    console.error("Failed to fetch order history:", e);
    ordersError.value = e.message;
  } finally {
    isOrdersLoading.value = false;
  }
}

onMounted(async () => {
  await fetchRiderData();
  if (rider.value && !error.value) {
    await fetchRiderOrderHistory();
  }
});

const goBack = () => { router.go(-1); };
const blockRider = () => { if (!rider.value) return; alert(`已将送餐员 ${rider.value.name} 加入黑名单 (模拟操作)`); };
const contactRider = () => {
  if (!rider.value) return;
  router.push({ name: 'ChatPage', params: { chatId: `chat_${rider.value.id}` } });
};
const likeRider = async () => {
  if (!rider.value || !rider.value.stats) return;
  try {
    const isCurrentlyLiked = isLikedByCurrentUser.value;
    const response = await riderAPI.likeRider(riderId.value, !isCurrentlyLiked);
    const result = response.data?.data; // API响应结构
    
    if (result) {
      rider.value.stats.likeCount = result.likeCount;
      isLikedByCurrentUser.value = result.isLiked;
      
      if (result.isLiked) {
        localStorage.setItem(`liked_rider_${riderId.value}`, 'true');
        alert(`已点赞 ${rider.value.name}!`);
      } else {
        localStorage.removeItem(`liked_rider_${riderId.value}`);
        alert(`已取消点赞 ${rider.value.name}`);
      }
    }
  } catch (error) {
    console.error("点赞操作失败:", error);
    alert("点赞操作失败，请稍后重试");
  }
};
const handleOrderReviewed = (reviewDetails) => {
  const orderIndex = riderOrderHistory.value.findIndex(o => o.orderId === reviewDetails.orderId);
  if (orderIndex !== -1) {
    riderOrderHistory.value[orderIndex].userReview = reviewDetails.review;
  }
};

</script>

<style scoped>
.rider-profile-page {
  display: flex;
  flex-direction: column;
  height: 900px;
  /* Full viewport height */
  max-width: 500px;
  margin: 0 auto;
  background-color: #f4f6f8;
}

.profile-page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  flex-shrink: 0;
  /* Prevent header from shrinking */
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.back-button svg {
  width: 15px;
  height: 15px;
  stroke: #555;
}

.page-title {
  margin: 0;
  color: #333;
  text-align: center;
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-placeholder {
  width: 40px;
  flex-shrink: 0;
}
.profile-content-scrollable {
  flex-grow: 1;
  overflow-y: auto;
  /* padding: 15px; */
  display: flex;
  flex-direction: column;
  /* 隐藏滚动条但保留滚动功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

/* Chrome/Safari/Opera */
.profile-content-scrollable::-webkit-scrollbar {
  display: none;
}
.loading-indicator,
.error-message,
.not-found {
  text-align: center;
  padding: 40px 20px;
  font-size: 1.1em;
  color: #555;
  flex-grow: 1;
  /* Take space if content is not loaded */
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: #d9534f;
}

.profile-content-scrollable {
  flex-grow: 1;
  /* Allow this area to grow and shrink */
  overflow-y: auto;
  /* Enable vertical scrolling for this section */
  padding: 15px;
  display: flex;
  flex-direction: column;
  /* Stack main layout and order history */
}

.profile-main-layout {
  display: flex;
  flex-direction: row;
  height:300px;
  gap: 15px;
  margin-bottom: 0px;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  align-items: stretch;
}

.left-column {
  flex: 6;  /* 原为1.2 */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.right-column {
  flex: 2;  /* 原为0.8 */
  display: flex;
  min-height: 100%;
  align-items: stretch;
}



/* RiderOrderHistory will naturally take full width below the profile-main-layout */

.profile-actions {
  position: fixed;
  /* Make footer sticky at the bottom of the viewport */
  bottom: 0;
  left: 0;
  /* Necessary for sticky within its parent if parent is not body */
  right: 0;
  width:100%;
  max-width: 370px;
  /* Match page max-width */
  margin: 0 auto;
  /* Center it if page is wider */
  display: flex;
  justify-content: space-around;
  background-color: #ffffff;
  padding: 12px 10px;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05);
  z-index: 100;
  /* Ensure it's above scrollable content */
  flex-shrink: 0;
  /* Prevent footer from shrinking */
}

/* Action button styles from previous example are fine */
.action-button {
  flex: 1;
  margin: 0 5px;
  padding: 10px 12px;
  font-size: 0.9em;
  border: 1px solid #ccc;
  border-radius: 20px;
  background-color: #f8f9fa;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
}

.action-button svg {
  margin-right: 6px;
}

.action-button:hover {
  background-color: #e9ecef;
  border-color: #bbb;
}

.action-button.block {
  color: #dc3545;
  border-color: #dc3545;
}

.action-button.block:hover {
  background-color: #dc3545;
  color: white;
}

.action-button.contact {
  color: #007bff;
  border-color: #007bff;
}

.action-button.contact:hover {
  background-color: #007bff;
  color: white;
}

.action-button.like {
  color: #28a745;
  border-color: #28a745;
}

.action-button.like.liked {
  background-color: #28a745;
  color: white;
}

.action-button.like:hover:not(.liked) {
  background-color: #28a745;
  color: white;
}
</style>