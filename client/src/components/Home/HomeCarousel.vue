// components/home/HomeCarousel.vue
<template>
  <div class="carousel-section">
    <a-carousel autoplay>
      <div v-for="(img, index) in images" :key="index">
        <img 
          :src="img.url" 
          :alt="img.alt" 
          :style="{ transform: `scale(${img.scale})` }"
          @error="handleImageError(index)"
        />
      </div>
    </a-carousel>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  images: {  
    type: Array,
    default: () => [
      { 
        url: new URL('/images/banner1.jpg', import.meta.url).href,
        alt: '广告1',
        scale: 1
      },
      { 
        url: new URL('/images/banner2.jpg', import.meta.url).href,
        alt: '广告2',
        scale: 1
      }
    ]
  }
});

// 图片错误处理
const handleImageError = (index) => {
  props.images[index].error = true;
};
</script>

<style scoped>
.carousel-section {
  margin: 10px 25px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 113px;
}

:deep(.ant-carousel .slick-slide) {
  height: 113px;
  overflow: hidden;
  text-align: center;
}

:deep(.ant-carousel .slick-slide img) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>