<template>
  <footer class="bottom-nav">
    <div 
      class="nav-item" 
      :class="{ active: $route.path === '/' }"
      @click="$router.push('/')">
      <span class="icon"><i class="fas fa-home"></i></span> 
      首页
    </div>
    <div 
      class="nav-item" 
      :class="{ active: $route.path === '/messages' }"
      @click="$router.push('/messages')">
      <span class="icon"><i class="fas fa-comment-alt"></i></span> 
      <!-- <span class="badge"></span>  -->
      消息
    </div>
    <div 
      class="nav-item" 
      :class="{ active: $route.path === '/profile' }"
      @click="$router.push('/profile')">
      <span class="icon"><i class="fas fa-user"></i></span> 
      我的
    </div>
  </footer>
</template>

<script setup>
import { useRoute } from 'vue-router'
const $route = useRoute()
</script>

<style scoped>
.bottom-nav {
  display: flex;
  justify-content: space-around;
  max-width: 390px;
  margin: 0 auto;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 15px 0;
  position: fixed;
  bottom: 0;
  width: 100%;
  box-shadow: 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 12px;
  color: #86868b;
  transition: all 0.2s ease;
}

.nav-item.active {
  color: #000000;
}

.nav-item .icon {
  font-size: 22px;
  margin-bottom: 4px;
  transition: transform 0.2s ease;
}

.nav-item:hover .icon {
  transform: scale(1.1);
}

.nav-item .badge {
  background-color: #ff3b30;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
</style>
