<template>
  <div class="page-container">
    <ProfilePortrait ></ProfilePortrait>
    <div class="profile-info">
      <div class="personal-info">
        <span class="icon1"><i class="fas fa-address-card"></i></span>
        <p class="description">个人资料</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/personal')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fa fa-google-wallet"></i></span>
        <p class="description">钱包/优惠券</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/wallet')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fas fa-bars"></i></span>
        <p class="description">历史订单</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/orders')"></i></span>
      </div>

      <div class="personal-info">
        <span class="icon1"><i class="fas fa-headphones"></i></span>
        <p class="description">联系客服</p>
        <span class="icon2"><i class="fas fa-angle-right"></i></span>
      </div>

      <div class="personal-info last-info">
        <span class="icon1"><i class="fas fa-certificate"></i></span>
        <p class="description">设置</p>
        <span class="icon2"><i class="fas fa-angle-right" @click="$router.push('/profile/settings')"></i></span>
      </div>
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
  background-color: #F7F8FA;
  padding: 20px;
  padding-bottom: 80px;
  min-height: 900px;
  box-sizing: border-box;
  text-align: center;
}

.profile-info {
  background-color: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
  text-align: left;
}

.personal-info {
  display: flex;
  align-items: center;
  padding: 18px 20px;
  border-top: 1px solid #F0F0F0;
}

.personal-info:first-child {
  border-top: none;
}

.last-info {
}

.icon1 {
  font-size: 22px;
  color: #5D6D7E;
  margin-right: 18px;
}

.description {
  flex-grow: 1;
  font-size: 1rem;
  color: #34495E;
  margin: 0;
}

.icon2 {
  font-size: 20px;
  color: #AEB6BF;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
}

.icon2:hover {
  color: #5D6D7E;
}
</style>