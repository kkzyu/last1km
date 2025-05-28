<template>
  <a-page-header
    title="订单详情"
    @back="handleBack"
    class="order-header"
  />
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.order-header {
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
</style>
