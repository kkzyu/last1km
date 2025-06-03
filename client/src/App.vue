<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();

onMounted(() => {
  userStore.fetchUserProfile();
});

</script>

<template>
  <div class="app-container">
    <div class="content-container">
      <RouterView />
    </div>
  </div>
</template>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 390px;
  margin: 0 auto;
  /* margin-bottom:20px; */
  border: 1px solid #e0e0e0;
  border-radius: 8px; /* Slightly rounded corners */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  overflow: hidden; /* Ensures child elements don't overflow rounded corners */
  position: relative;
}

.content-container {
  flex: 1;
  overflow: hidden;
  position: relative;

}
</style>