<script setup>
import { RouterView } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import TopHead from '@/components/TopHead.vue'
</script>

<template>
  <TopHead />
  <RouterView />
  <BottomNav />
</template>
