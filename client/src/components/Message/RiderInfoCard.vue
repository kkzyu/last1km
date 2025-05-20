<template>
  <div class="rider-info-card">
    <img :src="rider.avatar || '/avatars/default.png'" alt="Rider Avatar" class="rider-avatar-display">
    <h2 class="rider-name-display">{{ rider.name }}</h2>
    <p v-if="rider.bio" class="rider-bio-display">{{ rider.bio }}</p>
  </div>
</template>

<script setup>
defineProps({
  rider: {
    type: Object,
    required: true,
    default: () => ({ name: '加载中...', avatar: '', bio: '' })
  }
});
</script>

<style scoped>
.rider-info-card {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center avatar and name */
  text-align: center;
  padding-bottom: 15px; /* Space before stats panel */
}

.rider-avatar-display {
  width: 100px; /* Adjust as needed */
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e0e0e0;
  margin-bottom: 12px;
}

.rider-name-display {
  margin: 0 0 8px 0;
  font-size: 1.5em; /* Slightly larger */
  color: #2c3e50;
  font-weight: 600;
}

.rider-bio-display {
  font-size: 0.9em;
  color: #555;
  line-height: 1.4;
  margin: 0;
  max-width: 90%; /* Prevent bio from being too wide */
}
</style>