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
      :class="{ active: $route.path === '/orders' }"
      @click="$router.push('/orders')">
      <span class="icon"><i class="fas fa-comment-alt"></i></span> 
      <span class="badge">3</span> 
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
/* 复制原有的底部导航栏样式 */
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
  padding: 10px 0;
  position: fixed;
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
  position: relative;
}
.bottom-nav .nav-item.active {
  color: #1976D2;
}
.bottom-nav .nav-item .icon {
  font-size: 1.5em;
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
</style>
