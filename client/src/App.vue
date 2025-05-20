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
  /* margin-bottom:20px; */
  border: 1px solid #e0e0e0; /* Light gray border */
  border-radius: 8px; /* Slightly rounded corners */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  overflow: hidden; /* Ensures child elements don't overflow rounded corners */
}

.content-container {
  flex: 1;
  overflow: hidden;
  position: relative;
  border-top: 1px solid #e0e0e0; /* Separator between header and content */
}
</style>