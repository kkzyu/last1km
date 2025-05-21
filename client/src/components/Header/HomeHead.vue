<template>
  <header class="top-nav">
    <div class="logo">{{ title }}</div>
    <slot></slot>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '学士配送'
  }
});
</script>

<style scoped>
.top-nav {
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
}

.logo {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.5px;
  background: linear-gradient(45deg, #1d1d1f, #454545);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
