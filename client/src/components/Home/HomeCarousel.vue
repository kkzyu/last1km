<template>
 <section class="carousel-section">
    <div class="carousel-wrapper">
      <div 
        v-for="(img, index) in images" 
        :key="index"
        class="carousel-item"
        :class="{ active: currentIndex === index }"
      >
        <img
          :src="img.url"
          :alt="img.alt"
          :style="{ transform: `scale(${img.scale})` }"
          @error="handleImageError(index)"
        >
      </div>
    </div>
    
    <!-- 圆形切换控件 -->
    <div class="pagination">
      <button
        v-for="(_, index) in images"
        :key="index"
        :class="{ active: currentIndex === index }"
        @click="goToSlide(index)"
      />
    </div>
  </section>
</template>
<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  images: {  
    type: Array,
    default: () => [
      { 
        url: new URL('/images/banner1.jpg', import.meta.url).href,
        alt: '广告1',
        scale:1
      },
      { 
        url: new URL('/images/banner2.jpg', import.meta.url).href,
        alt: '广告2',
        scale:1
      }
    ]
  }
})

const currentIndex = ref(0)
const imageFailed = ref(false)

// 自动轮播逻辑
onMounted(() => {
  setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % props.images.length
  }, 3000)
})
// 跳转到指定幻灯片
const goToSlide = (index) => {
  currentIndex.value = index
}

// 图片错误处理
const handleImageError = (index) => {
  props.images[index].error = true
}
</script>

<style scoped>
.carousel-section {
  height: 150px;
  /* width: 700px; */
  position: relative;
  overflow: hidden; /* 隐藏溢出内容 */
  border-radius: 20px; /* 圆角 */
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* 阴影 */
  margin:25px;
}

.carousel-item {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 2s ease;
  
  &.active {
    opacity: 1;
  }
  
  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
}
/* 圆形分页控件 */
.pagination {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  
  button {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    
    &.active {
      background: white;
      transform: scale(1.2);
    }
    
    &:hover {
      background: white;
    }
  }
}

</style>
