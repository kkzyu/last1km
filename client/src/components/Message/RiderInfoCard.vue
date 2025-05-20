<template>
  <div class="rider-info-card">
    <img :src="rider.avatar || '/avatars/default.png'" alt="Rider Avatar" class="rider-avatar-display">
    <h3 class="rider-name-display">{{ rider.name }}</h3>
    <p v-if="rider.bio" class="rider-bio-display">{{ rider.bio }}</p>
  </div>
</template>

<script setup>
defineProps({
  rider: {
    type: Object,
    required: true,
    default: () => ({ name: '加载中...', avatar: '' })
  }
});
</script>

<style scoped>
.rider-info-card {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center avatar and name */
  text-align: center;
  padding-bottom: 10px; /* Space before stats panel */
}

.rider-avatar-display {
  width: 70px; /* Adjust as needed */
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e0e0e0;
  margin-bottom: 3px;
}

.rider-name-display {
  margin: 0 ;
  color: #2c3e50;
  font-weight: 600;
}

</style>