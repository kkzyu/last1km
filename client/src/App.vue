<script setup>
import { RouterView } from 'vue-router'

</script>

<template>
  <div class="app-container">
    <!-- <TopHead /> -->
    <div class="content-container">
      <RouterView />
    </div>
  </div>
</template>

<style>

.app-container {
  display: flex;
  flex-direction: column;
  height: 750px;
  max-width: 500px;
  margin: 0 auto;
}

.content-container {
  flex: 1;
  overflow: hidden;
  position: relative;
  
}
</style>