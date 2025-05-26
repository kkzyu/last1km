<template>
  <a-layout-header class="app-header">
    <div class="logo" v-html="title"></div>
    <slot></slot>
  </a-layout-header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ' <span class="zju-text">ZJU  </span> <span class="last1km-text">Last 1Km</span>'
  }
});
</script>

<style scoped>
.app-header {
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: #1d1d1f;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  height: auto;
  line-height: normal;
}

.logo {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.5px;
  /* background: linear-gradient(45deg, #1d1d1f, #454545); */
  /* -webkit-background-clip: text; */
  /* -webkit-text-fill-color: transparent; */
}

.logo ::v-deep(.last1km-text) {
  background: linear-gradient(45deg, #1d1d1f, #454545);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 24px;
}

.logo ::v-deep(.zju-text) {
  background: linear-gradient(45deg, #007bff, #0056b3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 24px;  
  font-weight: 550; 
}
</style>