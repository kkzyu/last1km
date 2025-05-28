// client/src/components/Header/BackHeader.vue
<template>
  <a-layout-header class="back-header">
    <a-button type="text" @click="goBack" class="back-button">
      <template #icon><ArrowLeftOutlined /></template>
    </a-button>
    <div class="header-title">{{ title }}</div>
    <div class="placeholder"></div>
  </a-layout-header>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ArrowLeftOutlined } from '@ant-design/icons-vue';
import axios from '@/plugins/axios';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: true
  }
});

const router = useRouter();
const goBack = () => router.go(-1);
</script>

<style scoped>
.back-header {
  display: flex;
  align-items: center;
  padding: 0 16px;
  background-color: #fff;
  height: 56px;
  line-height: 56px;
}

.back-button {
  font-size: 20px;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 500;
}

.placeholder {
  width: 32px;
}
</style>