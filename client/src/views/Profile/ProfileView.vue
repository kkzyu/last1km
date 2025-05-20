<template>
  <div class="page-container">
  </div>
  <ProfilePortrait></ProfilePortrait>
  <div class="profile-info">
    <div class="personal-info">
      <span class="icon1"><i class="fas fa-address-card"></i></span>
      <p class="description">个人资料</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/personal')"></i></span>
    </div>

    <div class="personal-info">
      <span class="icon1"><i class="fa fa-google-wallet"></i></span>
      <p class="description">钱包/优惠券</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/wallet')"></i></span>
    </div>

    <div class="personal-info">
      <span class="icon1"><i class="fas fa-bars"></i></span>
      <p class="description">历史订单</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/orders')"></i></span>
    </div>

    <div class="personal-info">
      <span class="icon1"><i class="fas fa-headphones"></i></span>
      <p class="description">联系客服</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info last-info">
      <span class="icon1"><i class="fas fa-certificate"></i></span>
      <p class="description">设置</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/settings')"></i></span>
    </div>
  </div>
  <BottomNav />
</template>

<script setup>
import ProfilePortrait from '@/components/Profile/ProfilePortrait.vue'
import BottomNav from '@/components/Bottom/BottomNav.vue'
import { useRoute } from 'vue-router'

const $route = useRoute()
</script>

<style scoped>
@import url("https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/font-awesome/4.7.0/css/font-awesome.min.css");

.page-container {
  padding: 20px;
  text-align: center;
}

.profile-info {
  display: flex;
  flex-direction: column;
  padding: 20px;
  /* width: 100%; */
}

.personal-info {
  display: flex;
  justify-content: flex-start;
  border-top: 1px solid #e0e0e0;
  align-items: center;
}

.last-info {
  border-bottom: 1px solid #e0e0e0;
}

.icon1 {
  font-size: 30px;
  padding: 0 10px 0 0;
  color:grey;
  width: 10%;
}

.description {
  width: 30%;
}

.empty-box {
  width: 50%;
}

.icon2 {
  font-size: 30px;
  color:grey;
  cursor: pointer;
}
</style>