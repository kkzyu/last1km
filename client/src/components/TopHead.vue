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
  background-color: #2196F3;
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.2em;
  font-weight: bold;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .logo {
    font-size: 1em;
  }
}
</style>
