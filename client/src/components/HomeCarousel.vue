<template>
  <section class="carousel-section">
    <div class="carousel-placeholder">
      <img
        v-if="!imageFailed"
        :src="imageUrl"
        :alt="altText"
        @error="handleImageError"
      >
      <div 
        v-else 
        class="image-failed"
      >
        {{ errorText }}
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  imageUrl: {
    type: String,
    default: 'https://via.placeholder.com/800x200'
  },
  altText: {
    type: String,
    default: '广告位'
  },
  errorText: {
    type: String,
    default: 'failed'
  }
})

const imageFailed = ref(false)

const handleImageError = () => {
  imageFailed.value = true
}
</script>

<style scoped>
.carousel-section {
  height: 200px;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-placeholder {
  height: 200px;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.carousel-section img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.image-failed {
  color: #666;
  font-size: 1.2em;
}
</style>
