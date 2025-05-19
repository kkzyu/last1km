<script setup>
import { RouterView } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import TopHead from '@/components/TopHead.vue'
</script>

<template>
  <div class="app-container">
    <TopHead />
    <div class="content-container">
      <RouterView />
    </div>
    <BottomNav />
  </div>
</template>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;

}

.content-container {
  flex: 1;
  overflow: hidden;
  position: relative;
}
</style>